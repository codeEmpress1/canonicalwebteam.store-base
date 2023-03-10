from flask import Blueprint, request, current_app as app

from canonicalwebteam.store_base.packages.logic import get_packages
from canonicalwebteam.store_base.utils.config import PACKAGE_PARAMS

package = Blueprint(
    "store",
    __name__,
)


@package.route("/store")
def store():
    app_name = app.name
    params = PACKAGE_PARAMS[app_name]
    store, fields, size = params["store"], params["fields"], params["size"]
    page = int(request.args.get("page", 1))
    return get_packages(store, fields, size, page)
