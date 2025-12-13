# backend/config/loader.py

from .settings import *


def get_setting(name: str, default=None):
    return globals().get(name, default)
