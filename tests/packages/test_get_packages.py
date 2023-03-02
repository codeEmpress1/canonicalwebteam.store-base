from flask_testing import TestCase
from tests.mock_data import sample_snap, sample_charm
from canonicalwebteam.store_base.packages.logic import get_packages, parse_package_for_card

class TestPackages(TestCase):

    def test_parse_package(self):
        snap_result = parse_package_for_card(sample_snap, "snap")
        charm_result = parse_package_for_card(sample_charm, "charm")
        self.assertEqual(snap_result["package"]["description"], sample_snap["snap"]["summary"])
        self.assertEqual(snap_result["package"]["display_name"], sample_snap["snap"]["title"])
        self.assertEqual(snap_result["package"]["type"], "snap")
        self.assertEqual(charm_result["package"]["description"], sample_charm["result"]["summary"])
        self.assertEqual(charm_result["package"]["display_name"], sample_charm["result"]["title"])
        self.assertEqual(charm_result["package"]["type"], "charm")
