from flask import session, redirect
from functools import wraps


def require_admin(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get("logged", False):
            return func(*args, **kwargs)
        return redirect("/admin/login")

    return inner
