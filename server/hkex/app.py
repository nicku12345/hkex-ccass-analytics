from flask import Flask
from flask_cors import CORS


class HKEXApp:

    @classmethod
    def CreateApp(cls, ENV="DEV"):

        app = Flask(__name__)

        if ENV == "DEV":
            from hkex.config.appsettings_dev import APPSETTINGS
        elif ENV == "TEST":
            from hkex.config.appsettings_test import APPSETTINGS
        elif ENV == "PROD":
            from hkex.config.appsettings_prod import APPSETTINGS
        else:
            raise Exception(f"{ENV} is not a valid environment")

        APPSETTINGS.ApplySettings(app)

        from hkex.database import DatabaseInitApp
        from hkex.managers import ManagersInitApp
        from hkex.controllers import ControllersInitApp

        DatabaseInitApp(app)
        ManagersInitApp(app)
        ControllersInitApp(app)

        CORS(app)
        cors = CORS(app, resouce={
            r"/*": {
                "origins": "*"
            }
        })

        return app
