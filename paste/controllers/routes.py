from bottle import abort, get, post, redirect, \
    request, response, static_file, view

from paste import settings
from paste.domain import AccessDenied, DoesNotExist, Snippet, User

from .services import snippet_service, user_service
from .utils import auth_required, get_current_user, \
    inject_user, not_found_handler


@get('/')
def index():
    redirect('/new')


@get('/last')
@view('list.html')
@inject_user
def last_snippets():
    return {'snippets': snippet_service.get_page()}


@get('/new')
@view('new.html')
@inject_user
def new_snippet_form():
    pass


@post('/new')
def new_snippet():
    snippet = snippet_service.create(Snippet(
        name=request.params.name,
        raw=request.params.raw,
        syntax=request.params.syntax,
        author=get_current_user(),
    ))
    redirect('/snippet/%s' % snippet.pk)


@get('/snippet/<pk:int>')
@view('snippet.html')
@inject_user
@not_found_handler
def get_snippet(pk):
    return {'snippet': snippet_service.get_by_pk(pk)}


@get('/snippet/<pk:int>/text')
@not_found_handler
def get_text_snippet(pk):
    response.content_type = 'text;charset=utf-8'
    return snippet_service.get_by_pk(pk).raw


@get('/user/<name>')
@view('list.html')
@inject_user
@not_found_handler
def user_snippets(name):
    user = user_service.get_by_name(name)
    return {'snippets': snippet_service.get_page(author=user)}


@get('/snippet/<pk:int>/delete')
@not_found_handler
@auth_required
def delete_snippet(user, pk):
    try:
        snippet_service.delete(user, snippet_service.get_by_pk(pk))
    except AccessDenied:
        abort(403)

    redirect('/user/' + user.name)


@get('/register')
@view('register.html')
def register_form():
    pass


@post('/register')
def register():
    user = user_service.register(User(
        name=request.forms.name, password=request.forms.password,
    ))

    response.set_cookie('user', user.pk, secret=settings.SECRET_KEY)
    redirect('/user/' + user.name)


@get('/login')
@view('login.html')
def login_form():
    pass


@post('/login')
def login():
    try:
        user = user_service.auth(
            request.forms.name, request.forms.password,
        )
    except DoesNotExist:
        redirect('/login')

    response.set_cookie('user', user.pk, secret=settings.SECRET_KEY)
    redirect('/user/' + user.name)


@get('/logout')
def logout():
    response.delete_cookie('user')
    redirect('/last')


# nginx in production
@get(r'/static/<path:path>')
def static(path):
    return static_file(path, settings.STATIC_PATH)
