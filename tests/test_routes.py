"""
Integration tests for web service
"""

import os
from unittest import TestCase

from migrator.application import migrator_factory
from webtest import AppError, TestApp

from paste import settings
from wsgi import app


def check_location(response, path):
    assert response.location == 'http://localhost:80' + path


class APITestCase(TestCase):

    def setUp(self):
        settings.DATABASE = '.test.db'
        migrator_factory(state_path='.test_migrator_state').apply(None)
        self.app = TestApp(app)

    def tearDown(self):
        os.remove('.test_migrator_state')
        os.remove('.test.db')


class IndexTestCase(APITestCase):

    """
    GET /
    """

    def test(self):
        response = self.app.get('/')
        assert response.status_code == 302
        check_location(response, '/new')


class GetSnippetTestCase(APITestCase):

    """
    GET /snippet/<pk:int>
    """

    def test_does_not_found(self):
        test_pk = 1
        with self.assertRaisesRegex(AppError, r'404'):
            self.app.get('/' + str(test_pk))


class LogoutTestCase(APITestCase):

    """
    GET /logout
    """

    def test(self):
        self.app.set_cookie('user', 'test_user')
        assert 'user' in self.app.cookies

        response = self.app.get('/logout')

        # check that cookie removed
        response.unset_cookie('user', strict=True)

        assert response.status_code == 302
        check_location(response, '/last')
