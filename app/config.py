import os
import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "nxkvndicms34cnhynecnwmn41"

JWT_AUTH_URL_RULE = "/api/login"
JWT_AUTH_ENDPOINT = "login"
JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=3600)