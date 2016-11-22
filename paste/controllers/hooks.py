from bottle import hook, request


@hook('before_request')
def strip_path():
    """
    Ignore trailing slashes in routes
    """
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')
