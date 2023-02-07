# canonicalwebteam.store-base

## ABOUT

This is a base application for all stores. It creates the applications and each store extends it with it's views and functionalities.

###USAGE

```
from canonicalwebteam.store_base.app import create_app

app = create_app(
    app_name,
    store_bp=store_blueprint 
)
```