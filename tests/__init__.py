# -*- coding: utf-8 -*-
"""
    Unit Tests
    ~~~~~~~~~~

    Define TestCase as base class for unit tests.
    Ref: http://packages.python.org/Flask-Testing/
"""

from flask.ext.testing import TestCase as Base

from rootio import create_app
from rootio.user import User, UserDetail, ADMIN, NETWORK_USER, ACTIVE
from rootio.config import TestConfig
from rootio.extensions import db
from rootio.utils import MALE


class TestCase(Base):
    """Base TestClass for your application."""

    def create_app(self):
        """Create and return a testing flask app."""

        app = create_app(TestConfig)
        return app

    def init_data(self):

        demo = User(
                name=u'demo',
                email=u'demo@example.com',
                password=u'123456',
                role_code=NETWORK_USER,
                status_code=ACTIVE,
                user_detail=UserDetail(
                    age=10,
                    url=u'http://demo.example.com',
                    location=u'Hangzhou',
                    bio=u'admin Guy is ... hmm ... just a demo guy.'))
        admin = User(
                name=u'admin',
                email=u'admin@example.com',
                password=u'123456',
                role_code=ADMIN,
                status_code=ACTIVE,
                user_detail=UserDetail(
                    age=10,
                    url=u'http://admin.example.com',
                    location=u'Hangzhou',
                    bio=u'admin Guy is ... hmm ... just a admin guy.'))
        db.session.add(demo)
        db.session.add(admin)
        db.session.commit()

    def setUp(self):
        """Reset all tables before testing."""

        db.create_all()
        self.init_data()

    def tearDown(self):
        """Clean db session and drop all tables."""

        db.drop_all()

    def login(self, username, password):
        data = {
            'login': username,
            'password': password,
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        return response

    def _logout(self):
        response = self.client.get('/logout')
        self.assertRedirects(response, location='/')

    def _test_get_request(self, endpoint, template=None):
        response = self.client.get(endpoint)
        self.assert_200(response)
        if template:
            self.assertTemplateUsed(name=template)
        return response
