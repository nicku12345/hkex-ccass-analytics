from hkex.config.base_appsettings import Appsettings
from hkex.config.secrets.ConnectionStrings import DEV_CONNECTION_STRING


APPSETTINGS = Appsettings(
    SQLALCHEMY_DATABASE_URI=DEV_CONNECTION_STRING,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=False,
    IS_TEST=False,
)
