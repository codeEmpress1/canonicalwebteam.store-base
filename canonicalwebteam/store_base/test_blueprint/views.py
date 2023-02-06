from flask import Blueprint

test_bp = Blueprint(
    "test_store_bp",
    __name__,

)

@test_bp.route("/test_store_bp")
def test_bp_route():
    return "This is a test blueprint on the storebase"