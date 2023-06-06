import talisker
import flask
from flask import (
    Blueprint,
    request,
    session,
    make_response,
    current_app as app,
)

from canonicalwebteam.store_base.packages.logic import (
    get_packages,
    get_snaps_account_info,
)
from canonicalwebteam.store_base.utils.config import PACKAGE_PARAMS

from canonicalwebteam.store_base.utils.decorators import login_required

store_packages = Blueprint(
    "package",
    __name__,
)


@store_packages.route("/store.json")
def get_store_packages():
    app_name = app.name
    params = PACKAGE_PARAMS[app_name]
    store, fields, size = params["store"], params["fields"], params["size"]
    page = int(request.args.get("page", 1))
    res = make_response(get_packages(store, fields, size, page))
    return res


@store_packages.route("/<any(charms, bundles, snaps):package_type>")
@login_required
def package(package_type):
    """
    Retrieves and returns package information based on the current app
    and package type.

    :returns: Response: The HTTP response containing the JSON data of the
    packages.
    """

    app_name = app.name
    publisher = PACKAGE_PARAMS[app_name]["publisher"]

    publisher_api = publisher(talisker.requests.get_session())

    if app_name.startswith("charmhub"):
        publisher_packages = publisher_api.get_account_packages(
            session["account-auth"], "charm", include_collaborations=True
        )
        page_type = request.path[1:-1]

        response = make_response(
            {
                "published_packages": [
                    package
                    for package in publisher_packages
                    if package["status"] == "published"
                    and package["type"] == page_type
                ],
                "registered_packages": [
                    package
                    for package in publisher_packages
                    if package["status"] == "registered"
                    and package["type"] == page_type
                ],
                "page_type": page_type,
            }
        )
        return response

    if app_name.startswith("snapcraft"):
        account_info = publisher_api.get_account(flask.session)

        user_snaps, registered_snaps = get_snaps_account_info(account_info)
        flask_user = flask.session["publisher"]

        response = make_response(
            {
                "snaps": user_snaps,
                "current_user": flask_user["nickname"],
                "registered_snaps": registered_snaps,
            }
        )

        return response