from flask_testing import TestCase
import responses
import requests
from pymacaroons import Macaroon
from canonicalwebteam.store_base.app import create_app

class LoginTest(TestCase):
    
    def __init__(self, api_url) -> super:
        return super().__init__(api_url)

    def setup(self, api_url):
        self.endpoint_url = "/login"
        self.api_url = api_url
    
    def create_app(self):
        app = create_app(testing=True)
        app.secret_key = "secret_key"
        app.config["WTF_CSRF_METHODS"] = []

        return app 

    @responses.activate
    def test_login_handler_redirect(self):
        m = Macaroon()
        m.add_third_party_caveat("login.ubuntu.com", "key", "id")

        serialized_macaroon = m.serialize()

        responses.add(
            responses.Response(
                method="POST",
                url=self.api_url,
                json={"macaroon": serialized_macaroon},
                status=200,
            )
        )

        response = self.client.get(self.endpoint_url)

        assert len(responses.calls) == 1
        assert response.status_code == 302

    @responses.activate
    def test_login_api_500(self):
        responses.add(
            responses.Response(method="POST", url=self.api_url, status=500)
        )

        response = self.client.get(self.endpoint_url)

        assert len(responses.calls) == 1
        assert response.status_code == 502

    @responses.activate
    def test_login_api_401(self):
        responses.add(
            responses.Response(method="POST", url=self.api_url, status=401)
        )

        response = self.client.get(self.endpoint_url)

        assert len(responses.calls) == 1
        assert response.status_code == 302
        self.assertEqual("http://localhost/logout", response.location)

    @responses.activate
    def test_login_connection_error(self):
        responses.add(
            responses.Response(
                method="POST",
                url=self.api_url,
                body=requests.exceptions.ConnectionError(),
                status=500,
            )
        )

        response = self.client.get(self.endpoint_url)

        assert response.status_code == 502
