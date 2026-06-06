"""
Décorateurs d'autorisation basés sur les rôles.
Permet de protéger certaines routes (ex : seuls les agents publient des biens).
"""
from functools import wraps
from flask import abort
from flask_login import current_user


def agent_required(view_func):
    """Autorise uniquement les agents et administrateurs."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_agent():
            abort(403)
        return view_func(*args, **kwargs)

    return wrapper


def admin_required(view_func):
    """Autorise uniquement les administrateurs."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return view_func(*args, **kwargs)

    return wrapper