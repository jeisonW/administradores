from flask import redirect, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "reset_token" not in session:
            return "Acceso no autorizado. Debes proporcionar un token válido."
        return f(*args, **kwargs)
    return decorated_function


def permisoempleado_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "permisoempleado" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def permisoproveedores(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "permisoproveedores" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function



def permisoventa(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "permisoventa" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


def permisocompra(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "permisocompra" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def permisodesperfecto(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "permisodesperfecto" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


def permisoproducto(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "permisoproducto" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


