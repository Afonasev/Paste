"""
Application settings
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_PATH = os.path.join(BASE_DIR, './static')
SECRET_KEY = os.environ.get('PASTE_SECRET_KEY', os.urandom(64))
DATABASE = os.environ.get('PASTE_DATABASE', 'db.sqlite3')
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
