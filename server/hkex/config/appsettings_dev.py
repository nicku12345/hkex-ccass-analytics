from hkex.config.base_appsettings import Appsettings


APPSETTINGS = Appsettings(
    SQLALCHEMY_DATABASE_URI="sqlite:///data/sqlite/db_dev.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_ECHO=False,
    IS_TEST=False,
)
