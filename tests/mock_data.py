sample_snap_api_response = {
    "name": "test_snap_data",
    "snap": {
        "media": [
            {
                "height": 512,
                "type": "icon",
                "url": "https://randomurl.com/icon.png",
                "width": 512,
            },
            {
                "height": 1365,
                "type": "banner",
                "url": "https://randomurl.com/banner.png",
                "width": 4095,
            },
            {
                "height": 1000,
                "type": "screenshot",
                "url": "https://randomurl.com/screenshot.png",
                "width": 1500,
            },
            {
                "height": 1000,
                "type": "screenshot",
                "url": "https://randomurl.com/screenshot.png",
                "width": 1500,
            },
            {
                "height": 1000,
                "type": "screenshot",
                "url": "https://randomurl.com/screenshot.png",
                "width": 1500,
            },
            {
                "height": 1000,
                "type": "screenshot",
                "url": "https://randomurl.com/screenshot.png",
                "width": 1500,
            },
            {
                "height": 1000,
                "type": "screenshot",
                "url": "https://randomurl.com/screenshot.png",
                "width": 1500,
            },
        ],
        "publisher": {
            "display-name": "Publisher Name",
            "id": "randompublisherID",
            "username": "publisher_name",
            "validation": "unproven",
        },
        "summary": "snap data",
        "title": "Test snap data",
        "categories": [{"name": "category name", "slug": "category-slug"}],
    },
    "snap-id": "somerandomID",
}

sample_snap_categories_response = {"name": "art-and-design"}

sample_charm_api_response = {
    "default-release": {
        "channel": {
            "base": {
                "architecture": "all",
                "channel": "20.04",
                "name": "ubuntu",
            },
            "name": "stable",
            "released-at": "released-at",
            "risk": "stable",
            "track": "latest",
        },
        "revision": {"revision": 123},
    },
    "id": "someID",
    "name": "A charm name",
    "result": {
        "title": "A charm title",
        "categories": [
            {
                "featured": False,
                "name": "category name",
                "slug": "category-slug",
            }
        ],
        "deployable-on": [],
        "media": [
            {
                "height": "",
                "type": "icon",
                "url": "https://randomurl.com/icon.png",
                "width": "",
            }
        ],
        "publisher": {"display-name": "Publisher name"},
        "summary": "A charm summary",
    },
    "type": "charm",
    "store_front": {
        "icons": ["https://randomurl.com/icon.png"],
        "deployable-on": [""],
        "categories": [
            {"featured": False, "name": "Databases", "slug": "databases"}
        ],
        "display-name": "Postgresql",
    },
}

sample_charm_list = {
    "results": [
        {
            "package": {
                "name": "test1",
                "platforms": ["VM", "kubernetes"],
                "type": "charm",
            },
            "publisher": {"display-name": "publisher test1"},
            "categories": [{"name": "cat-1", "display_name": "cat 1"}],
        },
        {
            "package": {"name": "test2", "platforms": ["VM"], "type": "charm"},
            "publisher": {"display-name": "publisher test2"},
            "categories": [{"name": "cat-2", "display_name": "cat 2"}],
        },
        {
            "package": {"name": "test9", "platforms": ["VM"], "type": "charm"},
            "publisher": {"display-name": "publisher test9"},
            "categories": [{"name": "cat-2", "display_name": "cat 2"}],
        },
        {
            "package": {
                "name": "test14",
                "platforms": ["kubernetes"],
                "type": "charm",
            },
            "publisher": {"display-name": "publisher test14"},
            "categories": [{"name": "cat-1", "display_name": "cat 1"}],
        },
        {
            "package": {
                "name": "test11",
                "platforms": ["kubernetes"],
                "type": "charm",
            },
            "publisher": {"display-name": "publisher test11"},
            "categories": [{"name": "cat-3", "display_name": "test cat 3"}],
        },
        {
            "package": {
                "name": "test3",
                "platforms": ["VM"],
                "type": "bundle",
            },
            "publisher": {"display-name": "publisher test3"},
            "categories": [{"name": "cat-3", "display_name": "cat 3"}],
        },
        {
            "package": {
                "name": "test4",
                "platforms": ["kubernetes"],
                "type": "bundle",
            },
            "publisher": {"display-name": "publisher test4"},
            "categories": [{"name": "cat-3", "display_name": "cat 3"}],
        },
        {
            "package": {
                "name": "test10",
                "platforms": ["kubernetes", "VM"],
                "type": "bundle",
            },
            "publisher": {"display-name": "publisher test10"},
            "categories": [{"name": "cat-3", "display_name": "test cat 3"}],
        },
        {
            "package": {
                "name": "test12",
                "platforms": ["VM"],
                "type": "bundle",
            },
            "publisher": {"display-name": "publisher test12"},
            "categories": [{"name": "cat-3", "display_name": "test cat 12"}],
        },
        {
            "package": {
                "name": "test13",
                "platforms": ["VM"],
                "type": "bundle",
            },
            "publisher": {"display-name": "publisher test13"},
            "categories": [{"name": "cat-1", "display_name": "cat 1"}],
        },
    ]
}

sample_snap_list = {
    "results": [
        {
            "package": {
                "name": "test15",
                "platforms": ["arch3"],
                "type": "snap",
            },
            "publisher": {"display-name": "publisher test15"},
            "categories": [{"name": "cat-1", "display_name": "cat 1"}],
        },
        {
            "package": {
                "name": "test5",
                "platforms": ["arch1"],
                "type": "snap",
            },
            "publisher": {"display-name": "publisher test5"},
            "categories": [{"name": "cat-3", "display_name": "cat 3"}],
        },
        {
            "package": {
                "name": "test6",
                "platforms": ["arch1"],
                "type": "snap",
            },
            "publisher": {"display-name": "publisher test6"},
            "categories": [{"name": "cat-2", "display_name": "cat 2"}],
        },
        {
            "package": {
                "name": "test7",
                "platforms": ["arch1", "arch2"],
                "type": "snap",
            },
            "publisher": {"display-name": "publisher test7"},
            "categories": [{"name": "cat-2", "display_name": "cat 2"}],
        },
        {
            "package": {
                "name": "test8",
                "platforms": ["arch2"],
                "type": "snap",
            },
            "publisher": {"display-name": "publisher test8"},
            "categories": [{"name": "cat-2", "display_name": "cat 2"}],
        },
    ]
}

sample_package_card = {
    "package": {
        "package": {
            "name": "test1",
            "platforms": ["VM", "kubernetes"],
            "type": "charm",
        },
        "publisher": {"display-name": "publisher test1"},
        "categories": [{"name": "cat-1", "display_name": "cat 1"}],
    }
}
sample_package_card2 = {
    "package": {
        "package": {
            "name": "test15",
            "platforms": ["arch3"],
            "type": "snap",
        },
        "publisher": {"display-name": "publisher test15"},
        "categories": [{"name": "cat-1", "display_name": "cat 1"}],
    }
}
