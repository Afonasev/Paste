#!/usr/bin/env python3
from bottle import default_app, TEMPLATE_PATH
from paste import settings
from paste.controllers import hooks, middlewares, routes  # noqa pylint: disable=unused-variable

app = default_app()
app.config.SECRET_KEY = settings.SECRET_KEY
TEMPLATE_PATH.append('./paste/controllers/templates/')

if __name__ == '__main__':
    app.run(debug=True, reloader=True)
