from .app import Application
from .endpoint import tg_update_handler


def setup_app(webhook_path: str) -> Application:
    app_ = Application()

    # TODO: setup routes, middlewares, etc.
    app_.router.add_post(webhook_path, tg_update_handler)

    # TODO: setup on startup, on shutdown, etc. handlers
    return app_
