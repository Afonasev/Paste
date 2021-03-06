from bottle import abort, redirect, request

from paste import domain, settings

from .services import user_service


def auth_required(f):
    def wrap(*args, **kw):
        user = get_current_user()
        if user is None:
            redirect('/login')
        return f(user, *args, **kw)
    return wrap


def not_found_handler(f):
    def wrap(*args, **kw):
        try:
            return f(*args, **kw)
        except domain.DoesNotExist:
            abort(404)
    return wrap


def inject_user(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs) or {}
        user = get_current_user()
        if user is not None:
            result['user'] = user
        return result
    return wrapper


def get_current_user():
    user_pk = request.get_cookie('user', secret=settings.SECRET_KEY)
    if user_pk is None:
        return None
    return user_service.get_by_pk(user_pk)
