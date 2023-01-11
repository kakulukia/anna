from .settings import *

STAGE = True

JAZZMIN_SETTINGS = {
    "site_logo": "img/mylogo-test-login.png" if STAGE else "img/mylogo-gruen-login.png",
    "site_icon": "assets/img/favicon-test.png" if STAGE else "assets/img/favicon.png",
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},

        {"name": f"Seite Anzeigen ({'STAGE' if STAGE else 'LIVE'})", "url": "index", "permissions": []},
        # model admin to link to (Permissions checked against model)
        {"model": "users.User"},
    ],
}
