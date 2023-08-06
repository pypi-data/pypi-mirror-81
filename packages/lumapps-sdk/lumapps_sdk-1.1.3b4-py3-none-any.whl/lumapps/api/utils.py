import os
from datetime import datetime, timedelta
from json import dumps, loads
from typing import Any, Dict, Optional, Sequence

from lumapps.api.conf import __pypi_packagename__

if not os.getenv("GAE_ENV"):  # noqa
    import sqlite3

    _sqlite_ok = True
else:
    _sqlite_ok = False


CACHE_MAX_AGE = timedelta(seconds=60 * 60 * 24)  # 1 day
GOOGLE_APIS = ("drive", "admin", "groupssettings")
FILTERS = {
    # content/get, content/list, ...
    "content/*": [
        "lastRevision",
        "authorDetails",
        "updatedByDetails",
        "writerDetails",
        "headerDetails",
        "customContentTypeDetails",
        "properties/duplicateContent",
        "excerpt",
    ],
    # community/get, community/list, ...
    "community/*": [
        "lastRevision",
        "authorDetails",
        "updatedByDetails",
        "writerDetails",
        "headerDetails",
        "customContentTypeDetails",
        "adminsDetails",
        "usersDetails",
    ],
    "communitytemplate/*": [
        "lastRevision",
        "authorDetails",
        "updatedByDetails",
        "writerDetails",
        "headerDetails",
        "customContentTypeDetails",
        "adminsDetails",
        "usersDetails",
    ],
    # template/get, template/list, ...
    "template/*": ["properties/duplicateContent"],
    "community/post/*": [
        "updatedByDetails",
        "mentionsDetails",
        "parentContentDetails",
        "headerDetails",
        "tagsDetails",
        "excerpt",
    ],
    "comment/get": ["authorProperties", "mentionsDetails"],
    "comment/list": ["authorProperties", "mentionsDetails"],
}


def pop_matches(dpath, d):
    if not dpath:
        return
    for pth_part in dpath.split("/")[:-1]:
        if not isinstance(d, dict):
            return
        d = d.get(pth_part)
    if not isinstance(d, dict):
        return
    d.pop(dpath.rpartition("/")[2], None)


def get_conf_db_file() -> str:
    if "APPDATA" in os.environ:
        d = os.environ["APPDATA"]
    elif "XDG_CONFIG_HOME" in os.environ:
        d = os.environ["XDG_CONFIG_HOME"]
    else:
        d = os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(d, "{}.db".format(__pypi_packagename__))


def _get_sqlite_ok():
    return _sqlite_ok


def _set_sqlite_ok(ok):
    global _sqlite_ok
    _sqlite_ok = ok


def _get_conn(db_file=None):
    if not _get_sqlite_ok():
        return None
    try:
        conn = sqlite3.connect(db_file or get_conf_db_file())
        conn.isolation_level = None
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS discovery_cache (
                url TEXT NOT NULL,
                expiry TEXT NOT NULL,
                content TEXT NOT NULL,
                PRIMARY KEY (url)
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS config (
                name TEXT NOT NULL,
                content TEXT NOT NULL,
                PRIMARY KEY (name)
            )"""
        )
        return conn
    except sqlite3.OperationalError:
        _set_sqlite_ok(False)
        return None


class ConfigStore:
    @staticmethod
    def get(name: str) -> Optional[Dict[str, Any]]:
        conn = _get_conn()
        if not conn:
            return None
        row = conn.execute(
            "SELECT content FROM config WHERE name=?", (name,)
        ).fetchone()
        return loads(row[0]) if row else None

    @staticmethod
    def get_names():
        conn = _get_conn()
        if not conn:
            return []
        return [r[0] for r in conn.execute("SELECT name FROM config")]

    @staticmethod
    def set(name: str, content: Any) -> None:
        conn = _get_conn()
        if not conn:
            return
        conn.execute(
            "INSERT OR REPLACE INTO config VALUES (?, ?)",
            (name, dumps(content, indent=4)),
        )


class DiscoveryCacheDict:
    def __init__(self):
        self._cache = {}

    def get(self, key, raises=False):
        if raises:
            cached = self._cache[key]
        else:
            cached = self._cache.get(key)
        if not cached or cached["expiry"] < datetime.now():
            return None
        return cached["value"]

    def set(self, key, value, ex=None):
        if ex:
            expiry = datetime.now() + timedelta(seconds=ex)
        else:
            expiry = datetime.now() + CACHE_MAX_AGE
        self._cache[key] = {"expiry": expiry, "value": value}


_DiscoveryCacheDict = DiscoveryCacheDict()


class DiscoveryCacheSqlite:
    def get(self, url):
        conn = _get_conn()
        if not conn:
            return _DiscoveryCacheDict.get(url)
        cached = conn.execute(
            "SELECT * FROM discovery_cache WHERE url=?", (url,)
        ).fetchone()
        if not cached:
            return None
        expiry_dt = datetime.strptime(cached["expiry"][:19], "%Y-%m-%dT%H:%M:%S")
        if expiry_dt < datetime.now():
            return None
        return loads(cached["content"])

    def set(self, url, content):
        conn = _get_conn()
        if not conn:
            _DiscoveryCacheDict.set(url, content)
            return
        expiry = (datetime.now() + CACHE_MAX_AGE).isoformat()[:19]
        conn.execute(
            "INSERT OR REPLACE INTO discovery_cache VALUES (?, ?, ?)",
            (url, expiry, dumps(content)),
        )


_discovery_cache: Any
if _sqlite_ok:
    _discovery_cache = DiscoveryCacheSqlite()
else:
    _discovery_cache = _DiscoveryCacheDict


def set_discovery_cache(cache):
    global _discovery_cache
    _discovery_cache = cache


def get_discovery_cache():
    return _discovery_cache


def list_prune_filters():
    s = ""
    for f in FILTERS:
        s += "\nMethods " + f + "\n"
        for pth in sorted(FILTERS[f]):
            s += "    " + pth + "\n"
    print("PRUNE FILTERS:\n" + s)


def _parse_endpoint_parts(parts):
    if len(parts) == 1:
        parts = parts[0].split("/")
    return parts


def method_from_discovery(
    discovery: Dict[str, Any], path: Sequence[str]
) -> Optional[Dict[str, Any]]:
    for part in path[:-1]:
        discovery = discovery["resources"].get(part)
        if not discovery:
            return None
    try:
        return discovery["methods"][path[-1]]
    except KeyError:
        return None


def walk_endpoints(resource, parents=()):
    for ep_name, ep_info in resource.get("methods", {}).items():
        yield tuple(parents + (ep_name,)), ep_info
    for rsc_name, rsc in resource.get("resources", {}).items():
        for ep_name, ep_info in walk_endpoints(rsc, tuple(parents + (rsc_name,))):
            yield ep_name, ep_info


def get_endpoints(discovery_doc):
    return {n: m for n, m in walk_endpoints(discovery_doc)}
