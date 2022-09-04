from hkex.controllers.ResourcesController import ResourcesController
from hkex.controllers.AnalyticsController import AnalyticsController

def ControllersInitApp(app):
    # app.register_blueprint(ConcreteController.blueprint)

    app.register_blueprint(ResourcesController.blueprint)
    app.register_blueprint(AnalyticsController.blueprint)
