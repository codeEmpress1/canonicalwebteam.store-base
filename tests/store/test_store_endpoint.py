import os
import responses
import unittest
from urllib.parse import urlencode
import json
from tests.mock_data import sample_package_list, sample_package_list2
from canonicalwebteam.store_base.app import create_app


class TestStoreEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.snaps_api_url = "".join(
            [
                "https://api.snapcraft.io/api/v2/",
                "snaps/find",
                "?",
                urlencode(
                    {"fields": "title,summary,media,publisher," "categories"}
                ),
            ]
        )

        self.charms_api_url = "".join(
            [
                "https://api.charmhub.io/v2/",
                "charms/find",
                "?q=&category=&publisher=&",
                urlencode(
                    {
                        "fields": "result.categories,result.summary,"
                        "result.media,result.title,"
                        "result.publisher.display-name,"
                        "default-release.revision.revision,"
                        "default-release.channel,"
                        "result.deployable-on"
                    }
                ),
            ]
        )

        self.endpoint_url = "/store.json"


class TestStoreEndpointWithCharmhub(TestStoreEndpoint):
    @responses.activate
    def test_store_endpoint_with_charmhub(self):
        os.environ["SECRET_KEY"] = "secret_key"
        app = create_app("charmhub", testing=True)
        app.name = "charmhub"
        app.config["WTF_CSRF_METHODS"] = []
        app.testing = True
        client = app.test_client()

        responses.add(
            responses.Response(
                method="GET",
                url=self.charms_api_url,
                body=json.dumps(sample_package_list),
                status=200,
            )
        )

        response = client.get(self.endpoint_url)

        self.assertEqual(response.status_code, 200)


class TestStoreEndpointWithSnapcraft(TestStoreEndpoint):
    def test_store_endpoint_with_snapcraft(self):
        os.environ["SECRET_KEY"] = "secret_key"
        app = create_app("snapcraft_beta", testing=True)
        app.name = "snapcraft_beta"
        app.config["WTF_CSRF_METHODS"] = []
        app.testing = True
        client = app.test_client()

        responses.add(
            responses.Response(
                method="GET",
                url=self.snaps_api_url,
                body=json.dumps(sample_package_list2),
                status=200,
            )
        )

        response = client.get(self.endpoint_url)

        self.assertEqual(response.status_code, 200)
