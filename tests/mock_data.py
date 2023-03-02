sample_snap = {
    "name": "test_snap_data",
        "snap": {
            "media": [
                {
                    "height": 512,
                    "type": "icon",
                    "url": "https://randomurl.com/icon.png",
                    "width": 512
                },
                {
                    "height": 1365,
                    "type": "banner",
                    "url": "https://randomurl.com/banner.png",
                    "width": 4095
                },
                {
                    "height": 1000,
                    "type": "screenshot",
                    "url": "https://randomurl.com/screenshot.png",
                    "width": 1500
                },
                {
                    "height": 1000,
                    "type": "screenshot",
                    "url": "https://randomurl.com/screenshot.png",
                    "width": 1500
                },
                {
                    "height": 1000,
                    "type": "screenshot",
                    "url": "https://randomurl.com/screenshot.png",                    "width": 1500
                },
                {
                    "height": 1000,
                    "type": "screenshot",
                    "url": "https://randomurl.com/screenshot.png",                    "width": 1500
                },
                {
                    "height": 1000,
                    "type": "screenshot",
                    "url": "https://randomurl.com/screenshot.png",                    "width": 1500
                }
            ],
            "publisher": {
                "display-name": "Publisher Name",
                "id": "randompublisherID",
                "username": "publisher_name",
                "validation": "unproven"
            },
            "summary": "Test snap data",
            "title": "Test snap data"
        },
        "snap-id": "somerandomID"
    }


sample_charm = {
    "default-release": {
        "channel": {
            "base": {
            "architecture": "all",
            "channel": "20.04",
            "name": "ubuntu"
            },
            "name": "stable",
            "released-at": "released-at",
            "risk": "stable",
            "track": "latest"
        },
        "revision": {
            "revision": 123
        }
    },
    "id": "someID",
    "name": "A charm name",
    "result": {
        "categories": [
            {
            "featured": False,
            "name": "category name",
            "slug": "category-slug"
            }
        ],
        "deployable-on": [],
        "media": [
            {
            "height": "",
            "type": "icon",
            "url": "https://randomurl.com/icon.png",
            "width": ""
            }
        ],
        "publisher": { "display-name": "Publisher name" },
        "summary": "A charm summary",
        "title": ""
    },
    "type": "charm",
    "store_front": {
        "icons": [
        "https://randomurl.com/icon.png"
        ],
        "deployable-on": [""],
        "categories": [
            { "featured": False, "name": "Databases", "slug": "databases" }
        ],
        "display-name": "Postgresql"
    }
}