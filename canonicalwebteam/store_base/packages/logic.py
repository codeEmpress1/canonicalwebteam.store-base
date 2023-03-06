import talisker
from flask import session, request, make_response
from typing import List, Dict, TypedDict, Any

from canonicalwebteam.store_api.exceptions import StoreApiError

from canonicalwebteam.store_base.utils import helpers


Package = TypedDict("Package_type", {"packages": List[Dict[str, Dict[str, str or List[str]] or List[Dict[str, str]]]]})


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


def paginate(packages: List[Package], page: int, size: int) -> List[Package]:

  start = (page - 1) * size
  end = start + size
  return packages[start:end]


def get_packages(store, fields: List[str], size: int=10, page: int=1) -> List[Dict[str, Any]]:
  """
  Returns a list of packages based on the given params
  Packages returns are paginated and parsed
  """

  packages = fetch_packages(store, fields).get("packages", [])
  packages_per_page = paginate(packages, size, page)
  parsed_packages = []
  for package in packages_per_page:
      parsed_packages.append(parse_package_for_card(package, package["type"]))
      
  return parsed_packages