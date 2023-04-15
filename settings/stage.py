from .common import *  # noqa

STAGE = True

JAZZMIN_SETTINGS["site_logo"] = (  # noqa
    "img/mylogo-test-login.png" if STAGE else "img/mylogo-gruen-login.png"
)
JAZZMIN_SETTINGS["site_icon"] = (  # noqa
    "assets/img/favicon-test.png" if STAGE else "assets/img/favicon.png"
)
JAZZMIN_SETTINGS["topmenu_links"] = [  # noqa
    {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
    {
        "name": f"Seite Anzeigen ({'STAGE' if STAGE else 'LIVE'})",
        "url": "index",
        "permissions": [],
    },
    {"model": "users.User"},
]

HUEY = {
    # To run Huey in "immediate" mode with a live storage API, specify
    "immediate_use_memory": False,
    # To run Huey in "live" mode regardless of whether DEBUG is enabled,
    "immediate": False,
    "connection": {
        "host": "localhost",
        "port": 6379,
        "db": 2,  # different DB for stage
    },
}
