import datetime
import talisker
from flask import session, request, make_response
from typing import List, Dict, TypedDict, Any

from canonicalwebteam.store_api.exceptions import StoreApiError

from canonicalwebteam.store_base.utils import helpers


Package = TypedDict(
    "Package_type",
    {
        "packages": List[
            Dict[str, Dict[str, str or List[str]] or List[Dict[str, str]]]
        ]
    },
)


def fetch_packages(store_api, fields: List[str]):
    """
    Fetch store packages, could be snaps, charms or bundles
    """

    store = store_api(talisker.requests.get_session())
    packages = store.find(fields=fields).get("results", [])
    response = make_response({"packages": packages})
    response.cache_control.max_age = 3600
    return response.json


def parse_package_for_card(package: Dict[str, Any], package_type) -> Package:
    """
    Takes a package (snap, charm or bundle) as input
    Returns the formatted package based on the given card schema
    """
    resp = {
        "package": {
            "description": "",
            "display_name": "",
            "icon_url": "",
            "name": "",
            "platforms": [],
            "type": "",
        },
        "publisher": {"display_name": "", "name": "", "validation": ""},
        "categories": [],
        # hardcoded temporarily until we have this data from the API
        "ratings": {"value": "0", "count": "0"},
    }

    if package_type == "snap":
        snap = package.get("snap", {})
        publisher = snap.get("publisher", {})
        resp["package"]["description"] = snap.get("summary", "")
        resp["package"]["display_name"] = snap.get("title", "")
        resp["package"]["type"] = "snap"
        resp["package"]["name"] = package.get("name", "")
        # platform to be fetched
        # resp["package"]["platforms"] = package["store_front"]["deployable-on"]
        resp["publisher"]["display_name"] = publisher.get("display-name", "")
        resp["publisher"]["name"] = publisher.get("username", "")
        resp["publisher"]["validation"] = publisher.get("validation", "")
        resp["categories"] = snap.get("categories", [])
        resp["package"]["icon_url"] = helpers.get_icon(
            package["snap"]["media"]
        )

    if package_type == "charm" or package_type == "bundle":
        result = package.get("result", {})
        publisher = result.get("publisher", {})
        
        resp["package"]["type"] = package.get("type", "")
        resp["package"]["name"] = package.get("name", "")
        resp["package"]["description"] = result.get("summary", "")
        resp["package"]["display_name"] = format_slug(result.get("display_name", ""))
        resp["package"]["platforms"] = result.get("deployable-on", [])
        resp["publisher"]["display_name"] = publisher.get("display-name", "")
        resp["publisher"]["validation"] = publisher.get("validation", "")
        resp["categories"] = result.get("categories", [])
        resp["package"]["icon_url"] = helpers.get_icon(result.get("media", []))

    return resp


def paginate(
    packages: List[Package], page: int, size: int, total_pages: int
) -> List[Package]:
    
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
    store, fields: List[str], size: int = 10, page: int = 1
) -> List[Dict[str, Any]]:
    """
    Returns a list of packages based on the given params
    Packages returns are paginated and parsed
    """

    packages = fetch_packages(store, fields).get("packages", [])
    total_pages = -(len(packages) // -size)
    packages_per_page = paginate(packages, page, size, total_pages)
    parsed_packages = []
    for package in packages_per_page:
        parsed_packages.append(
            parse_package_for_card(package, package["type"])
        )

    return {"packages": parsed_packages, "total_pages": total_pages}


def filter_packages(
    packages: List[Package], filter_params: Dict[str, List[str]]
):
    result = packages
    for key, val in filter_params.items():
        if key == "categories" and not "all" in val:
            result = list(
                filter(
                    lambda package: len(
                        [
                            cat
                            for cat in package["categories"]
                            if cat["name"] in val
                        ]
                    )
                    != 0,
                    result,
                )
            )
        if (key == "platforms" or key == "architectures") and not "all" in val:
            result = list(
                filter(
                    lambda package: len(
                        [p for p in package["platforms"] if p in val]
                    )
                    != 0,
                    result,
                )
            )

        if key == "type" and not "all" in val:
            result = list(
                filter(lambda package: package["package_type"] in val, result)
            )

    return result


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
    :returns: A list of categories in the format: [{"name": "Category", "slug": "category"}]
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
    Fetch all store categories
    """
    store = store_api(talisker.requests.get_session())
    try:
        all_categories = store.get_categories()
    except StoreApiError:
        all_categories = []

    return all_categories


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
