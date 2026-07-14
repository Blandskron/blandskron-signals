import os

from .base import *  # noqa: F403

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")  # noqa: F405
