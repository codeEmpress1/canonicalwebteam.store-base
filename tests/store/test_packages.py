import unittest
from tests.mock_data import (
    sample_snap_api_response,
    sample_charm_api_response,
    sample_charm_list,
)
from canonicalwebteam.store_base.packages.logic import (
    parse_package_for_card,
    paginate,
)
from canonicalwebteam.store_api.stores.charmstore import (
    CharmStore,
    CharmPublisher,
)
from canonicalwebteam.store_api.stores.snapstore import (
    SnapStore,
    SnapPublisher,
)


class TestPackages(unittest.TestCase):
    def test_parse_package(self):
        snap_result = parse_package_for_card(
            sample_snap_api_response, "snapcraft", SnapStore, SnapPublisher
        )
        charm_result = parse_package_for_card(
            sample_charm_api_response, "charmhub", CharmStore, CharmPublisher
        )

        self.assertEqual(
            snap_result["package"]["description"],
            sample_snap_api_response["snap"]["summary"],
        )
        self.assertEqual(
            snap_result["package"]["display_name"],
            sample_snap_api_response["snap"]["title"],
        )
        self.assertEqual(snap_result["package"]["type"], "snap")
        self.assertEqual(
            charm_result["package"]["description"],
            sample_charm_api_response["result"]["summary"],
        )
        self.assertEqual(
            charm_result["package"]["display_name"],
            sample_charm_api_response["result"]["title"],
        )
        self.assertEqual(charm_result["package"]["type"], "charm")

    def test_paginate(self):
        size1 = 5
        size2 = 3
        total_pages1 = -(len(sample_charm_list) // -size1)
        total_pages2 = -(len(sample_charm_list) // -size2)
        self.assertEqual(
            len(
                paginate(sample_charm_list["results"], 1, size1, total_pages1)
            ),
            5,
        )
        self.assertEqual(
            len(
                paginate(sample_charm_list["results"], 2, size2, total_pages2)
            ),
            3,
        )
