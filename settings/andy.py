from .common import *  #noqa

DEBUG = True
STAGE = True

JAZZMIN_SETTINGS["site_logo"] = "img/mylogo-test-login.png" if STAGE else "img/mylogo-gruen-login.png"
JAZZMIN_SETTINGS["site_icon"] = "assets/img/favicon-test.png" if STAGE else "assets/img/favicon.png"
JAZZMIN_SETTINGS["topmenu_links"] = [
    {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
    {"name": f"Seite Anzeigen ({'STAGE' if STAGE else 'LIVE'})", "url": "index", "permissions": []},
    {"model": "users.User"},
]
