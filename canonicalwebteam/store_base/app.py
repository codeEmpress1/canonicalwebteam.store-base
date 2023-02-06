"""
Extensible flask application base for all stores.

Its gets response from the store_api and it extends each store blueprint to make a complete application
"""
import yamlloader
# from canonicalwebteam.candid import FlaskBas
from canonicalwebteam.flask_base.app import FlaskBase
import canonicalwebteam.store_base.config as config
from canonicalwebteam.store_base.utils.extensions import csrf
from canonicalwebteam.store_base.test_blueprint.views import test_bp


"""

config would be passed in at store level

a default config is supplied.
"""
def create_app(app_name, favicon_url="", store_bp=test_bp, testing=False):

    app = FlaskBase(
    __name__,
    app_name,
    template_folder="../templates",
    favicon_url=favicon_url,
    )

    app.register_blueprint(store_bp)
    # app.config.from_object(config)
    app.testing = testing

    csrf.init_app(app)

    return app