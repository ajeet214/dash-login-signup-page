from .auth_callbacks import register_auth_callbacks
from .validation_callbacks import register_validation_callbacks


def register_callbacks(app):
    register_auth_callbacks(app)
    register_validation_callbacks(app)
