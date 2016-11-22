from unittest import TestCase

from webtest import TestApp

import wsgi


class AppTestCase(TestCase):

    def setUp(self):
        self.app = TestApp(wsgi.app)


class DummyTestCase(AppTestCase):

    def test(self):
        response = self.app.get('/new')
        assert response.status_code == 200
