import talisker
from typing import List, Dict, TypedDict, Any

from canonicalwebteam.store_api.exceptions import StoreApiError

from canonicalwebteam.store_base.utils import helpers


Package = TypedDict("Package_type", {"packages": List[Dict[str, Dict[str, str or List[str]] or List[Dict[str, str]]]]})



"""
Fetch store packages, could be snaps, charms or bundles
"""
def get_packages(store_publisher, fields, size, page=1) -> List[Dict[str, Any]]:
    
    publisher_api = store_publisher(talisker.requests.get_session())
    packages = publisher_api.find(fields=fields).get("results", [])
    parsed_packages = []
    for package in packages:
        parsed_packages.append(parse_package_for_card(package, package["type"]))
        
    return parsed_packages



"""
Takes a package (snap, charm or bundle) as input

Returns the formatted package based on the given card schema
"""
def parse_package_for_card(package: Dict[str, Any], package_type) -> Package:
    resp = {
      "package": {
        "description": "",
        "display_name": "",
        "icon_url": "",
        "name": "",
        "platforms": [],
        "type": ""
      },
      "publisher": {
        "display_name": "",
        "name": "",
        "validation": ""
      },
      "categories": []
    }

    if package_type == "snap":
        resp["package"]["description"] = package["snap"]["summary"]
        resp["package"]["display_name"] = package["snap"]["title"]
        resp["package"]["type"] = "snap"
        resp["package"]["name"] = package["name"]
        # platform to be fetched
        # resp["package"]["platforms"] = package["store_front"]["deployable-on"]
        resp["publisher"]["display_name"] = package["snap"]["publisher"]["display-name"]
        resp["publisher"]["name"] = package["snap"]["publisher"]["username"]
        resp["publisher"]["validation"] = package["snap"]["publisher"]["validation"]
        resp["categories"] = package["snap"]["categories"]
        resp["package"]["icon_url"] = helpers.get_icon(package["snap"]["media"])

    if package_type == "charm" or package_type == "bundle":
        resp["package"]["description"] = package["result"]["summary"]
        resp["package"]["display_name"] = package["display-name"]
        resp["package"]["type"] = package["type"]
        resp["package"]["name"] = package["name"]
        resp["package"]["platforms"] = package["store_front"]["deployable-on"]
        resp["publisher"]["display_name"] = package["result"]["publisher"]["display-name"]
        # resp["publisher"]["validation"] = package["publisher"]["validation"]
        resp["categories"] = package["store_front"]["categories"]
        resp["package"]["icon_url"] = helpers.get_icon(package["result"]["media"])

    return resp
