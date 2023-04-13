import unittest
from canonicalwebteam.store_base.utils import helpers


class TestHelpers(unittest.TestCase):
    def test_is_safe_url(self):
        """Should return True if url starts with /"""
        url = "/gosomewhere"
        self.assertEqual(helpers.is_safe_url(url), True)

    def test_modify_headers(self):
        pass

    def test_decrease_header(self):
        self.assertEqual(
            helpers.decrease_header({"name": "h2"}, 2), {"name": "h4"}
        )
        self.assertEqual(
            helpers.decrease_header({"name": "h5"}, 2), {"name": "h6"}
        )
        self.assertEqual(
            helpers.decrease_header({"name": "h6"}, 1), {"name": "h6"}
        )
        self.assertEqual(
            helpers.decrease_header({"name": "h1"}, 1), {"name": "h2"}
        )

    def test_add_header_id(self):
        h = {"name": "h2", "text": "some random text"}
        levels = []
        self.assertEqual(
            helpers.add_header_id(h, levels),
            {
                "name": "h2",
                "text": "some random text",
                "id": "some random text",
            },
        )
