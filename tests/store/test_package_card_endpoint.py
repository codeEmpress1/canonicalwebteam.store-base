import os
import responses
import unittest
from urllib.parse import urlencode
import json
from tests.mock_data import (
    sample_charm_api_response,
    sample_snap_api_response,
)
from canonicalwebteam.store_base.app import create_app


class TestPackageCardEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.snap_api_url = "".join(
            [
                "https://api.snapcraft.io/api/v1/",
                "snaps/info/",
                "test",
                "?",
                urlencode(
                    {"fields": "title,summary,media,publisher,categories"}
                ),
            ]
        )

        self.charm_api_url = "".join(
            [
                "https://api.charmhub.io/v2/",
                "charms/info/",
                "test",
                "?",
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

        self.endpoint_url = "/test/card.json"


class TestPackageCardEndpointWithCharmhub(TestPackageCardEndpoint):
    @responses.activate
    def test_package_endpoint_with_charmhub(self):
        os.environ["SECRET_KEY"] = "secret_key"
        app = create_app("charmhub_beta", testing=True)
        app.name = "charmhub_beta"
        app.config["WTF_CSRF_METHODS"] = []
        app.testing = True
        client = app.test_client()

        responses.add(
            responses.Response(
                method="GET",
                url=self.charm_api_url,
                body=json.dumps(sample_charm_api_response),
                status=200,
            )
        )

        response = client.get(self.endpoint_url)

        self.assertEqual(response.status_code, 200)


class TestPackageCardEndpointWithSnapcraft(TestPackageCardEndpoint):
    @responses.activate
    def test_package_endpoint_with_snapcraft(self):
        os.environ["SECRET_KEY"] = "secret_key"
        app = create_app("snapcraft_beta", testing=True)
        app.name = "snapcraft_beta"
        app.config["WTF_CSRF_METHODS"] = []
        app.testing = True
        client = app.test_client()

        responses.add(
            responses.Response(
                method="GET",
                url=self.snap_api_url,
                body=json.dumps(sample_snap_api_response),
                status=200,
            )
        )

        response = client.get(self.endpoint_url)

        self.assertEqual(response.status_code, 200)
