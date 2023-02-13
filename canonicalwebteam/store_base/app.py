"""
Extensible flask application base for all stores.

It gets response from the store_api and it extends

each store blueprint to make a complete application
"""
from flask import session, make_response
from canonicalwebteam.flask_base.app import FlaskBase
import canonicalwebteam.store_base.utils.config as config
from canonicalwebteam.store_base.utils.extensions import csrf
from canonicalwebteam.store_base.sample_blueprint.views import sample_bp
from canonicalwebteam.store_base.auth.login.views import login


"""
config would be passed in at store level a default config is supplied.
"""


def create_app(app_name, store_bp=sample_bp, testing=False):

    app = FlaskBase(__name__, app_name)

    app.register_blueprint(store_bp)
    app.config.from_object(config)
    app.testing = testing

    csrf.init_app(app)

    app.register_blueprint(login)

    @app.route("/account.json")
    def get_account_json():
        """
        A JSON endpoint to request login status
        """
        publisher = None
        
        if "publisher" in session:
            publisher = session["publisher"]

        response = {"publisher": publisher}
        response = make_response(response)
        response.headers["Cache-Control"] = "no-store"

        return response

    return app
