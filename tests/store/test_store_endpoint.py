import os
import responses
import unittest
from urllib.parse import urlencode
import json
from tests.mock_data import (
    sample_charm_list,
    sample_snap_api_response,
    sample_snap_categories_response,
)
from canonicalwebteam.store_base.app import create_app
import functools
import flask


def login_required_test(func):
    @functools.wraps(func)
    def is_user_logged_in(*args, **kwargs):
        if "publisher" not in flask.session:
            return flask.redirect(f"/login?next=/beta/{flask.request.path}")
        return func(*args, **kwargs)

    return is_user_logged_in


class TestStoreEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.snaps_api_url = "".join(
            [
                "https://api.snapcraft.io/v2/",
                "snaps/find",
                "?",
                urlencode(
                    {
                        "featured": "false",
                        "fields": "title,summary,media,publisher,categories",
                    }
                ),
            ]
        )

        self.snaps_categories_api_url = "".join(
            [
                "https://api.snapcraft.io/v2/",
                "snaps/categories",
            ]
        )

        self.charms_categories_api_url = "".join(
            [
                "https://api.charmhub.io/v2/",
                "charms/categories",
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
        app = create_app("charmhub_beta", login_required_test, testing=True)
        app.name = "charmhub_beta"
        app.config["WTF_CSRF_METHODS"] = []
        app.testing = True
        client = app.test_client()

        responses.add(
            responses.Response(
                method="GET",
                url=self.charms_categories_api_url,
                body=json.dumps(
                    {"categories": [sample_snap_categories_response]}
                ),
                status=200,
            )
        )

        responses.add(
            responses.Response(
                method="GET",
                url=self.charms_api_url,
                body=json.dumps(sample_charm_list),
                status=200,
            )
        )

        response = client.get(self.endpoint_url)

        self.assertEqual(response.status_code, 200)


class TestStoreEndpointWithSnapcraft(TestStoreEndpoint):
    @responses.activate
    def test_store_endpoint_with_snapcraft(self):
        os.environ["SECRET_KEY"] = "secret_key"
        app = create_app("snapcraft_beta", login_required_test, testing=True)
        app.name = "snapcraft_beta"
        app.config["WTF_CSRF_METHODS"] = []
        app.testing = True
        client = app.test_client()

        responses.add(
            responses.Response(
                method="GET",
                url=self.snaps_categories_api_url,
                body=json.dumps(
                    {"categories": [sample_snap_categories_response]}
                ),
                status=200,
            )
        )

        responses.add(
            responses.Response(
                method="GET",
                url=self.snaps_api_url,
                body=json.dumps({"results": [sample_snap_api_response]}),
                status=200,
            )
        )

        response = client.get(self.endpoint_url)

        self.assertEqual(response.status_code, 200)
