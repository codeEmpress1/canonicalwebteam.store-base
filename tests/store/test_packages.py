import unittest
from tests.mock_data import (
    sample_snap,
    sample_charm,
    sample_package_list,
    sample_package_list2,
)
from canonicalwebteam.store_base.packages.logic import (
    filter_packages,
    parse_package_for_card,
    paginate,
)


class TestPackages(unittest.TestCase):
    def test_parse_package(self):
        snap_result = parse_package_for_card(sample_snap)
        charm_result = parse_package_for_card(sample_charm)

        self.assertEqual(
            snap_result["package"]["description"],
            sample_snap["snap"]["summary"],
        )
        self.assertEqual(
            snap_result["package"]["display_name"],
            sample_snap["snap"]["title"],
        )
        self.assertEqual(snap_result["package"]["type"], "snap")
        self.assertEqual(
            charm_result["package"]["description"],
            sample_charm["result"]["summary"],
        )
        self.assertEqual(
            charm_result["package"]["display_name"],
            sample_charm["result"]["title"],
        )
        self.assertEqual(charm_result["package"]["type"], "charm")

    def test_paginate(self):
        size1 = 5
        size2 = 3
        total_pages1 = -(len(sample_package_list) // -size1)
        total_pages2 = -(len(sample_package_list) // -size2)
        self.assertEqual(
            len(
                paginate(
                    sample_package_list["results"], 1, size1, total_pages1
                )
            ),
            5,
        )
        self.assertEqual(
            len(
                paginate(
                    sample_package_list["results"], 2, size2, total_pages2
                )
            ),
            3,
        )

    def test_filter_packages(self):
        filter_params1 = {
            "categories": ["all", "cat-1"],
            "platforms": ["all", "VM"],
            "type": ["all", "charm"],
        }
        filter_params2 = {
            "categories": ["cat-1", "cat-3"],
            "platforms": ["VM", "kubernetes"],
            "type": ["charm"],
        }
        filter_params3 = {
            "categories": ["cat-2", "cat-3"],
            "platforms": ["kubernetes"],
            "type": ["charm"],
        }
        filter_params4 = {
            "categories": ["cat-2", "cat-3"],
            "platforms": ["kubernetes"],
            "type": ["bundle"],
        }
        filter_params5 = {
            "categories": ["cat-2"],
            "platforms": ["arch1"],
            "type": ["snap"],
        }

        self.assertEqual(
            len(
                filter_packages(sample_package_list["results"], filter_params1)
            ),
            10,
        )
        self.assertEqual(
            len(
                filter_packages(sample_package_list["results"], filter_params2)
            ),
            3,
        )
        self.assertEqual(
            len(
                filter_packages(sample_package_list["results"], filter_params3)
            ),
            1,
        )
        self.assertEqual(
            len(
                filter_packages(sample_package_list["results"], filter_params4)
            ),
            2,
        )
        self.assertEqual(
            len(
                filter_packages(
                    sample_package_list2["results"], filter_params5
                )
            ),
            2,
        )
