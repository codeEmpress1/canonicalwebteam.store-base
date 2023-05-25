Usage 
=====

Example::

    from canonicalwebteam.store_base.app import create_app

    import store-specific blueprint
    import store-specific utility processor

    app = create_app(
        "app_name",
        store_bp=store-specific blueprint,
        utility_processor=store-specific utility_processor,
    )

    app.static_folder=app_static_folder
    app.template_folder=app_template_folder
    app.static_url_path=app_static_url_path

    # all other store blueprints and configurations should be registered here
    # When the store app is run, all endpoints will be available at store-url/endpoint-url
 
