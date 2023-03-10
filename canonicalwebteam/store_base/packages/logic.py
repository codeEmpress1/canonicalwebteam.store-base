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
    return response


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
    }

    if package_type == "snap":
        resp["package"]["description"] = package["snap"]["summary"]
        resp["package"]["display_name"] = package["snap"]["title"]
        resp["package"]["type"] = "snap"
        resp["package"]["name"] = package["name"]
        # platform to be fetched
        # resp["package"]["platforms"] = package["store_front"]["deployable-on"]
        resp["publisher"]["display_name"] = package["snap"]["publisher"][
            "display-name"
        ]
        resp["publisher"]["name"] = package["snap"]["publisher"]["username"]
        resp["publisher"]["validation"] = package["snap"]["publisher"][
            "validation"
        ]
        resp["categories"] = package["snap"]["categories"]
        resp["package"]["icon_url"] = helpers.get_icon(
            package["snap"]["media"]
        )

    if package_type == "charm" or package_type == "bundle":
        resp["package"]["description"] = package["result"]["summary"]
        resp["package"]["display_name"] = package["store_front"][
            "display-name"
        ]
        resp["package"]["type"] = package["type"]
        resp["package"]["name"] = package["name"]
        resp["package"]["platforms"] = package["store_front"]["deployable-on"]
        resp["publisher"]["display_name"] = package["result"]["publisher"][
            "display-name"
        ]
        # resp["publisher"]["validation"] = package["publisher"][
        # "validation"
        # ]
        resp["categories"] = package["store_front"]["categories"]
        resp["package"]["icon_url"] = helpers.get_icon(
            package["result"]["media"]
        )

    return resp


def paginate(
    packages: List[Package], page: int, size: int, total_pages: int
) -> List[Package]:
    if page < 1 or page > total_pages:
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
    packages_per_page = paginate(packages, size, page, total_pages)
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


def format_category_name(slug):
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
                {"slug": category, "name": format_category_name(category)}
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
