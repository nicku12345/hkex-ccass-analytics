from flask import Flask
import logging
from dataclasses import dataclass
from logging.handlers import TimedRotatingFileHandler
import coloredlogs

@dataclass
class Appsettings:
    # General settings
    SQLALCHEMY_DATABASE_URI         : str
    SQLALCHEMY_TRACK_MODIFICATIONS  : bool
    SQLALCHEMY_ECHO                 : bool = False
    IS_TEST                         : bool = False
    ENVIRONMENT                     : str = "DEV"

    def ApplySettings(self, app: Flask):

        app.config["SQLALCHEMY_DATABASE_URI"] = self.SQLALCHEMY_DATABASE_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = self.SQLALCHEMY_TRACK_MODIFICATIONS
        app.config["SQLALCHEMY_ECHO"] = self.SQLALCHEMY_ECHO
        app.config["IS_TEST"] = self.IS_TEST
        app.config["ENVIRONMENT"] = self.ENVIRONMENT

        self.ApplyLoggingSettings(app)

    def ApplyLoggingSettings(self, app):
        '''
        Apply the logging settings to the app.
        It mainly manages the werkzeug (the default logger from the framework)
        and the flask app logger.
        '''
        app.logger.handlers.clear()

        # Werkzeug logger settings
        werkzeug_logger = logging.getLogger("werkzeug")
        werkzeug_logger.handlers.clear()

        # flask app logger settings
        flask_app_logger = logging.getLogger("flask.app")
        flask_app_logger.handlers.clear()

        # common stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)

        # formatter of the stream handler
        flask_app_formatter = logging.Formatter('[%(asctime)s] %(levelname)s: \t%(message)s')

        # apply the formatter to all handlers
        stream_handler.setFormatter(flask_app_formatter)

        flask_app_logger.addHandler(stream_handler)
        # add this handler only if it is not test
        werkzeug_logger.addHandler(stream_handler)

        coloredlogs.install(logger=flask_app_logger, level=logging.DEBUG)
        coloredlogs.install(logger=werkzeug_logger, level=logging.DEBUG)