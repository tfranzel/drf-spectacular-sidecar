import base64
import hashlib
import json
from typing import Optional
from urllib.request import urlopen

STATIC_PATH = "drf_spectacular_sidecar/static/drf_spectacular_sidecar"
JSDELIVR_META_URL = "https://data.jsdelivr.com/v1/package/npm"
JSDELIVR_DATA_URL = "https://cdn.jsdelivr.net/npm"

FILES = {
    "redoc": [
        "bundles/redoc.standalone.js",
    ],
    "swagger-ui-dist": [
        "swagger-ui-bundle.js",
        "swagger-ui-standalone-preset.js",
        "oauth2-redirect.html",
        "swagger-ui.css",
        "favicon-32x32.png",
    ]
}

with open("distributions.json") as fh:
    _CURRENT_VERSIONS = json.load(fh)


def get_jsdelivr_tags(package, tag) -> str:
    url = f"{JSDELIVR_META_URL}/{package}"
    data = json.loads(urlopen(url).read())
    return data["tags"][tag]


def get_jsdelivr_package_content(package, version) -> dict:
    url = f"{JSDELIVR_META_URL}/{package}@{version}"
    return json.loads(urlopen(url).read())


def parse_jsdelivr_package_tree(node, path=""):
    path = (path + "/" if path else "") + node.get("name", "")
    if "default" in node or node["type"] == "directory":
        for i in node["files"]:
            yield from parse_jsdelivr_package_tree(i, path)
    elif node["type"] == "file":
        yield path, node["hash"]


def get_file_hash(file) -> str:
    with open(file, "rb") as fh:
        return base64.b64encode(hashlib.sha256(fh.read()).digest()).decode()


def validated_download(url, target, expected_hash) -> None:
    path = f"{STATIC_PATH}/{target}"
    print(f"download {url} to {target} [{expected_hash}]")
    with open(path, "wb") as fh:
        fh.write(urlopen(url).read())
    assert get_file_hash(path) == expected_hash


def update_dist(package, tag) -> Optional[str]:
    old_version = _CURRENT_VERSIONS[package]
    new_version = get_jsdelivr_tags(package, tag)
    print(f"'{package}' package tag '{tag}' has version '{new_version}'")
    if new_version <= old_version:
        print(f"'{package}' package is up-to-date")
        return None
    package_hashes = dict(
        parse_jsdelivr_package_tree(get_jsdelivr_package_content(package, new_version))
    )
    for asset in FILES[package]:
        validated_download(
            url=f"{JSDELIVR_DATA_URL}/{package}@{new_version}/{asset}",
            target=f"{package}/{asset}",
            expected_hash=package_hashes[asset],
        )
    print(f"updated '{package}' from {old_version} to {new_version}")
    _CURRENT_VERSIONS[package] = new_version
    with open("distributions.json", 'w') as fh:
        json.dump(_CURRENT_VERSIONS, fh, indent=4)
    return new_version


def update_redoc() -> tuple[str, Optional[str]]:
    old_version = _CURRENT_VERSIONS["redoc"]
    return old_version, update_dist(package="redoc", tag="latest")


def update_swagger_ui() -> tuple[str, Optional[str]]:
    old_version = _CURRENT_VERSIONS["swagger-ui-dist"]
    return old_version, update_dist(package="swagger-ui-dist", tag="latest")
