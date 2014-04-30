# -*- coding: utf-8 -*-

import os

from utils import make_dir

# Get app root path, also can use flask.root_path.
# ../../config.py
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
INSTANCE_FOLDER_PATH = os.path.join(PROJECT_ROOT, 'instance')

class BaseConfig(object):
    PROJECT = "rootio"

    DEBUG = True
    TESTING = False

    ADMINS = ['admin@rootio.org','robotic@gmail.com','josh@levinger.net']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = os.environ.get("SECRET_KEY","SeekritKey__ChangeMe!!!oneoneone")

    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')
    make_dir(LOG_FOLDER)

    # File upload, should override in production.
    # Limited the maximum allowed payload to 16 megabytes.
    # http://flask.pocoo.org/docs/patterns/fileuploads/#improving-uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'uploads')
    make_dir(UPLOAD_FOLDER)

    ZMQ_SOCKET_TYPE = "PUB"
    ZMQ_BIND_ADDR = "ipc:///tmp/zmq.sock"

class DefaultConfig(BaseConfig):
    DEBUG = False
    CSRF_ENABLED = False

    # Flask-Sqlalchemy: http://packages.python.org/Flask-SQLAlchemy/config.html
    SQLALCHEMY_ECHO = False
    # Postgres for production.
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:NLPog1986@localhost'

    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = {#'ach':'Acholi',
                        'en':'English',
                        #'kdj':'Karamjong',
                        #'mhd':"Ma'di",
                        'nyn':'Nyankore',
                        'lug':'Luganda',
                        'luo':'Luo',}

    # Flask-cache: http://pythonhosted.org/Flask-Cache/
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # Flask-mail: http://pythonhosted.org/flask-mail/
    # https://bitbucket.org/danjac/flask-mail/issue/3/problem-with-gmails-smtp-server
    MAIL_DEBUG = DEBUG
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # Should put MAIL_USERNAME and MAIL_PASSWORD in production under instance folder.
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME",'gmail_username')
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD",'gmail_password')
    DEFAULT_MAIL_SENDER = '%s@gmail.com' % MAIL_USERNAME

    # Flask-openid: http://pythonhosted.org/Flask-OpenID/
    OPENID_FS_STORE_PATH = os.path.join(INSTANCE_FOLDER_PATH, 'openid')
    make_dir(OPENID_FS_STORE_PATH)


class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://' # store db in memory
