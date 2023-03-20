from flask import request


def get_macaroon_response(app_name, publisher_api):
    """
    returns macaroon response for store
    """
    if app_name.startswith("charmhub"):
        user_agent = request.headers.get("User-Agent")
        macaroon_response = publisher_api.issue_macaroon(
            [
            "account-register-package",
            "account-view-packages",
            "package-manage",
            "package-view",
        ],
        description=f"charmhub.io - {user_agent}",
        )
        authenticated_user_redirect = "store.store_packages"
        exchange_macaroon_method = publisher_api.exchange_macaroons
    if app_name.startswith("snapcraft"):
        macaroon_response = "macaroon"
        authenticated_user_redirect = "store.index"
        exchange_macaroon_method = publisher_api.exchange_dashboard_macaroon
    return {
        "macaroon_response":macaroon_response,
        "user_redirect":authenticated_user_redirect,
        "exchange_macaroon_method":exchange_macaroon_method,
    }