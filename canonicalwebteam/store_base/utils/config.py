import os

from canonicalwebteam.store_api.stores.charmstore import (
    CharmStore,
    CharmPublisher,
)
from canonicalwebteam.store_api.stores.snapstore import (
    SnapStore,
    SnapPublisher,
)

ENVIRONMENT = os.getenv("ENVIRONMENT", "devel")
SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")

# we want to ensure the keys matches the app name for each store for now
PACKAGE_PARAMS = {
    "snapcraft_beta": {
        "store": SnapStore,
        "publisher": SnapPublisher,
        "fields": [
            "title",
            "summary",
            "media",
            "publisher",
            "categories",
        ],
        "permissions": [
            "edit_account",
            "package_access",
            "package_metrics",
            "package_register",
            "package_release",
            "package_update",
            "package_upload_request",
            "store_admin",
        ],
        "size": 15,
    },
    "charmhub_beta": {
        "store": CharmStore,
        "publisher": CharmPublisher,
        "fields": [
            "result.categories",
            "result.summary",
            "result.media",
            "result.title",
            "result.publisher.display-name",
            "default-release.revision.revision",
            "default-release.channel",
            "result.deployable-on",
        ],
        "permissions": [
            "account-register-package",
            "account-view-packages",
            "package-manage",
            "package-view",
        ],
        "size": 12,
    },
}
