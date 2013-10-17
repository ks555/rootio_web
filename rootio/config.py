# -*- coding: utf-8 -*-

import os

from utils import make_dir, INSTANCE_FOLDER_PATH


class BaseConfig(object):

    PROJECT = "rootio"

    # Get app root path, also can use flask.root_path.
    # ../../config.py
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    ADMINS = ['admin@rootio.org','robotic@gmail.com','josh@levinger.net']

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = getattr(os.environ,'SECRET_KEY','SeekritKey-ReplaceMe!')

    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')
    make_dir(LOG_FOLDER)

    # File upload, should override in production.
    # Limited the maximum allowed payload to 16 megabytes.
    # http://flask.pocoo.org/docs/patterns/fileuploads/#improving-uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'uploads')
    make_dir(UPLOAD_FOLDER)


class DefaultConfig(BaseConfig):

    DEBUG = True

    # Flask-Sqlalchemy: http://packages.python.org/Flask-SQLAlchemy/config.html
    SQLALCHEMY_ECHO = True
    # SQLITE for prototyping.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + INSTANCE_FOLDER_PATH + '/db.sqlite'
    # Postgres for production.
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost'

    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = {#'ach':'Acholi',
                        'en':'English',
                        #'kdj':'Karamjong',
                        #'mhd':"Ma'di",
                        'nyn':'Nyankore',
                        'lug':'Luganda',
                        'luo':'Luo',}
    BABEL_DEFAULT_LOCALE = 'en' #see http://cldr.unicode.org/index/cldr-spec/picking-the-right-language-code
                                #abd http://unicode.org/cldr/utility/languageid.jsp
    # Flask-cache: http://pythonhosted.org/Flask-Cache/
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # Flask-mail: http://pythonhosted.org/flask-mail/
    # https://bitbucket.org/danjac/flask-mail/issue/3/problem-with-gmails-smtp-server
    MAIL_DEBUG = DEBUG
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # Should put MAIL_USERNAME and MAIL_PASSWORD in production environment variables
    MAIL_USERNAME = getattr(os.environ,'MAIL_USERNAME','gmail_username')
    MAIL_PASSWORD = getattr(os.environ,'MAIL_PASSWORD','gmail_password')
    DEFAULT_MAIL_SENDER = '%s@gmail.com' % MAIL_USERNAME

    # Flask-openid: http://pythonhosted.org/Flask-OpenID/
    OPENID_FS_STORE_PATH = os.path.join(INSTANCE_FOLDER_PATH, 'openid')
    make_dir(OPENID_FS_STORE_PATH)


class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
