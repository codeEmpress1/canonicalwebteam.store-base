import datetime
import re

import yaml

import talisker
from flask import make_response
from typing import List, Dict, TypedDict, Any

from canonicalwebteam.store_api.exceptions import StoreApiError

from canonicalwebteam.store_base.utils import helpers


Packages = TypedDict(
    "Packages_type",
    {
        "packages": List[
            Dict[str, Dict[str, str or List[str]] or List[Dict[str, str]]]
        ]
    },
)

Package = TypedDict(
    "Package_type",
    {
        "package": Dict[
            str, Dict[str, str or List[str]] or List[Dict[str, str]]
        ]
    },
)


def fetch_packages(store_api, fields: List[str], query_params) -> Packages:
    """
    Fetches packages from the store API based on the specified fields.

    :param: store_api: The specific store API object.
    :param: fields (List[str]): A list of fields to include in the package
    data.
    :param: query_params: A search query

    :returns: a dictionary containing the list of fetched packages.
    """
    store = store_api(talisker.requests.get_session())

    category = query_params.get("categories", "")
    query = query_params.get("q", "")
    package_type = query_params.get("type", None)
    platform = query_params.get("platforms", "")
    architecture = query_params.get("architecture", "")

    if package_type == "all":
        package_type = None

    args = {
        "category": category,
        "fields": fields,
        "query": query,
    }

    if package_type:
        args["type"] = package_type

    packages = store.find(**args).get("results", [])

    if platform and platform != "all":
        filtered_packages = []
        for p in packages:
            platforms = p["result"].get("deployable-on", [])
            if not platforms:
                platforms = ["vm"]
            if platform in platforms:
                filtered_packages.append(p)
        packages = filtered_packages

    if architecture and architecture != "all":
        args["architecture"] = architecture
        packages = store.find(**args).get("results", [])

    return packages


def fetch_package(store_api, package_name: str, fields: List[str]) -> Package:
    """
    Fetches a package from the store API based on the specified package name.

    :param: store_api: The specific store API object.
    :param: package_name (str): The name of the package to fetch.
    :param: fields (List[str]): A list of fields to include in the package

    :returns: a dictionary containing the fetched package.
    """
    store = store_api(talisker.requests.get_session())
    package = store.get_item_details(
        name=package_name,
        fields=fields,
        api_version=2,
    )
    response = make_response({"package": package})
    response.cache_control.max_age = 3600
    return response.json


def get_bundle_charms(charm_apps):
    result = []

    if charm_apps:
        for app_name, data in charm_apps.items():
            # Charm names could be with the old prefix/suffix
            # Like: cs:~charmed-osm/mariadb-k8s-35
            name = data["charm"]
            if name.startswith("cs:") or name.startswith("ch:"):
                name = re.match(r"(?:cs:|ch:)(?:.+/)?(\S*?)(?:-\d+)?$", name)[
                    1
                ]

            charm = {"display_name": format_slug(name), "name": name}

            result.append(charm)

    return result


def parse_package_for_card(
    package: Dict[str, Any],
    store_name: str,
    store_api: Any,
    publisher_api: Any,
    libraries: bool = False,
) -> Package:
    """
    Parses a package (snap, charm, or bundle) and returns the formatted package
    based on the given card schema.

    :param: package (Dict[str, Any]): The package to be parsed.
    :returns: a dictionary containing the formatted package.

    note:
        - This function has to be refactored to be more generic,
        so we won't have to check for the package type before parsing.

    """
    store = store_api(talisker.requests.get_session())
    publisher_api = publisher_api(talisker.requests.get_session())
    resp = {
        "package": {
            "description": "",
            "display_name": "",
            "icon_url": "",
            "name": "",
            "platforms": [],
            "type": "",
            "channel": {
                "name": "",
                "risk": "",
                "track": "",
            },
        },
        "publisher": {"display_name": "", "name": "", "validation": ""},
        "categories": [],
        # hardcoded temporarily until we have this data from the API
        "ratings": {"value": "0", "count": "0"},
    }

    if store_name.startswith("charmhub"):
        result = package.get("result", {})
        publisher = result.get("publisher", {})
        channel = package.get("default-release", {}).get("channel", {})
        risk = channel.get("risk", "")
        track = channel.get("track", "")
        if libraries:
            resp["package"]["libraries"] = publisher_api.get_charm_libraries(
                package["name"]
            ).get("libraries", [])
        resp["package"]["type"] = package.get("type", "")
        resp["package"]["name"] = package.get("name", "")
        resp["package"]["description"] = result.get("summary", "")
        resp["package"]["display_name"] = result.get(
            "title", format_slug(package.get("name", ""))
        )
        resp["package"]["channel"]["risk"] = risk
        resp["package"]["channel"]["track"] = track
        resp["package"]["channel"]["name"] = f"{track}/{risk}"
        resp["publisher"]["display_name"] = publisher.get("display-name", "")
        resp["publisher"]["validation"] = publisher.get("validation", "")
        resp["categories"] = result.get("categories", [])
        resp["package"]["icon_url"] = helpers.get_icon(result.get("media", []))

        platforms = result.get("deployable-on", [])
        if platforms:
            resp["package"]["platforms"] = platforms
        else:
            resp["package"]["platforms"] = ["vm"]

        if resp["package"]["type"] == "bundle":
            name = package["name"]
            default_release = store.get_item_details(
                name, fields=["default-release"]
            )
            bundle_yaml = default_release["default-release"]["revision"][
                "bundle-yaml"
            ]

            bundle_details = yaml.load(bundle_yaml, Loader=yaml.FullLoader)
            bundle_charms = get_bundle_charms(
                bundle_details.get(
                    "applications", bundle_details.get("services", [])
                )
            )
            resp["package"]["charms"] = bundle_charms

    if store_name.startswith("snapcraft"):
        snap = package.get("snap", {})
        publisher = snap.get("publisher", {})
        resp["package"]["description"] = snap.get("summary", "")
        resp["package"]["display_name"] = snap.get("title", "")
        resp["package"]["type"] = "snap"
        resp["package"]["name"] = package.get("name", "")
        # platform to be fetched
        resp["publisher"]["display_name"] = publisher.get("display-name", "")
        resp["publisher"]["name"] = publisher.get("username", "")
        resp["publisher"]["validation"] = publisher.get("validation", "")
        resp["categories"] = snap.get("categories", [])
        resp["package"]["icon_url"] = helpers.get_icon(
            package["snap"]["media"]
        )

    return resp


def paginate(
    packages: List[Packages], page: int, size: int, total_pages: int
) -> List[Packages]:
    """
    Paginates a list of packages based on the specified page and size.

    :param: packages (List[Packages]): The list of packages to paginate.
    :param: page (int): The current page number.
    :param: size (int): The number of packages to include in each page.
    :param: total_pages (int): The total number of pages.
    :returns: a list of paginated packages.

    note:
        - If the provided page exceeds the total number of pages, the last
        page will be returned.
        - If the provided page is less than 1, the first page will be returned.
    """

    if page > total_pages:
        page = total_pages
    if page < 1:
        page = 1

    start = (page - 1) * size
    end = start + size
    if end > len(packages):
        end = len(packages)

    return packages[start:end]


def get_packages(
    store,
    publisher: Any,
    store_name: str,
    libraries: bool,
    fields: List[str],
    size: int = 10,
    query_params: Dict[str, Any] = {},
) -> List[Dict[str, Any]]:
    """
    Retrieves a list of packages from the store based on the specified
    parameters.The returned packages are paginated and parsed using the
    card schema.

    :param: store: The store object.
    :param: fields (List[str]): A list of fields to include in the
            package data.
    :param: size (int, optional): The number of packages to include
            in each page. Defaults to 10.
    :param: page (int, optional): The current page number. Defaults to 1.
    :param: query (str, optional): The search query.
    :param: filters (Dict, optional): The filter parameters. Defaults to {}.
    :returns: a dictionary containing the list of parsed packages and
            the total pages
    """

    packages = fetch_packages(store, fields, query_params)

    total_pages = -(len(packages) // -size)

    total_pages = -(len(packages) // -size)
    total_items = len(packages)
    page = int(query_params.get("page", 1))
    packages_per_page = paginate(packages, page, size, total_pages)
    parsed_packages = []
    for package in packages_per_page:
        parsed_packages.append(
            parse_package_for_card(
                package, store_name, store, publisher, libraries
            )
        )
    res = parsed_packages

    categories = get_store_categories(store)

    return {
        "packages": res,
        "total_pages": total_pages,
        "total_items": total_items,
        "categories": categories,
    }


def format_slug(slug):
    """Format category name into a standard title format

    :param slug: The hypen spaced, lowercase slug to be formatted
    :return: The formatted string
    """
    return (
        slug.title()
        .replace("-", " ")
        .replace("And", "and")
        .replace("Iot", "IoT")
    )


def parse_categories(
    categories_json: Dict[str, List[Dict[str, str]]]
) -> List[Dict[str, str]]:
    """
    :param categories_json: The returned json from store_api.get_categories()
    :returns: A list of categories in the format:
    [{"name": "Category", "slug": "category"}]
    """

    categories = []

    if "categories" in categories_json:
        for category in categories_json["categories"]:
            categories.append(
                {"slug": category, "name": format_slug(category)}
            )

    return categories


def get_store_categories(store_api) -> List[Dict[str, str]]:
    """
    Fetches all store categories.

    :param: store_api: The store API object used to fetch the categories.
    :returns: A list of categories in the format:
    [{"name": "Category", "slug": "category"}]
    """
    store = store_api(talisker.requests.get_session())
    try:
        all_categories = store.get_categories()
    except StoreApiError:
        all_categories = []

    for cat in all_categories["categories"]:
        cat["display_name"] = format_slug(cat["name"])

    categories = list(
        filter(
            lambda cat: cat["name"] != "featured", all_categories["categories"]
        )
    )

    return categories


def get_snaps_account_info(account_info):
    """Get snaps from the account information of a user

    :param account_info: The account informations

    :return: A list of snaps
    :return: A list of registred snaps
    """
    user_snaps = {}
    registered_snaps = {}
    if "16" in account_info["snaps"]:
        snaps = account_info["snaps"]["16"]
        for snap in snaps.keys():
            if snaps[snap]["status"] != "Revoked":
                if not snaps[snap]["latest_revisions"]:
                    registered_snaps[snap] = snaps[snap]
                else:
                    user_snaps[snap] = snaps[snap]

    now = datetime.datetime.utcnow()

    for snap in user_snaps:
        snap_info = user_snaps[snap]
        for revision in snap_info["latest_revisions"]:
            if len(revision["channels"]) > 0:
                snap_info["latest_release"] = revision
                break

    if len(user_snaps) == 1:
        for snap in user_snaps:
            snap_info = user_snaps[snap]
            revisions = snap_info["latest_revisions"]

            revision_since = datetime.datetime.strptime(
                revisions[-1]["since"], "%Y-%m-%dT%H:%M:%SZ"
            )

            if abs((revision_since - now).days) < 30 and (
                not revisions[0]["channels"]
                or revisions[0]["channels"][0] == "edge"
            ):
                snap_info["is_new"] = True

    return user_snaps, registered_snaps


def get_package(
    store,
    publisher_api,
    store_name: str,
    package_name: str,
    fields: List[str],
    libraries: bool,
) -> Package:
    """Get a package by name

    :param store: The store object.
    :param store_name: The name of the store.
    :param package_name: The name of the package.
    :param fields: The fields to fetch.

    :return: A dictionary containing the package.
    """
    package = fetch_package(store, package_name, fields).get("package", {})
    resp = parse_package_for_card(
        package, store_name, store, publisher_api, libraries
    )
    return {"package": resp}
