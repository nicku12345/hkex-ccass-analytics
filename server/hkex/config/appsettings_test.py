from hkex.config.base_appsettings import Appsettings


APPSETTINGS = Appsettings(
    SQLALCHEMY_DATABASE_URI="sqlite:///data/sqlite/db_unittest.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=False,
    IS_TEST=False,
)
