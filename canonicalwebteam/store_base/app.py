"""
Extensible flask application base for all stores.

It gets response from the store_api and it extends

each store blueprint to make a complete application
"""
from canonicalwebteam.flask_base.app import FlaskBase
import canonicalwebteam.store_base.utils.config as config
from canonicalwebteam.store_base.packages.views import init_packages
from canonicalwebteam.store_base.utils.extensions import csrf
from canonicalwebteam.store_base.handlers import set_handlers
from canonicalwebteam.store_base.sample_blueprint.views import sample_bp


def create_app(
    app_name,
    login_required,
    store_bp=sample_bp,
    utility_processor=None,
    testing=False,
):
    app = FlaskBase(__name__, app_name)

    app.register_blueprint(store_bp)

    app.config.from_object(config)
    app.config["LOGIN_REQUIRED"] = login_required
    app.testing = testing
    csrf.init_app(app)
    set_handlers(app, utility_processor)
    init_packages(app)

    return app
