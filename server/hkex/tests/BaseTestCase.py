
from flask_testing import TestCase

from hkex.app import HKEXApp
from hkex.database import db
from hkex.database.models.Participant import Participant
from hkex.database.models.ShareHolding import ShareHolding



class BaseTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._db = db
        self._app = self.create_app()

    def create_app(self):
        return HKEXApp.CreateApp(ENV="TEST")

    def setUp(self):
        self.CleanDatabase()
        self._db.init_app(self._app)
        self.SetUpDatabase()

    def tearDown(self):
        self._db.session.remove()
        self.CleanDatabase()

    def CleanDatabase(self):
        database_uri = self._app.config["SQLALCHEMY_DATABASE_URI"]
        if not database_uri.endswith("test.db"):
            raise f"Database {database_uri} is not a test database!"

        self._db.session.query(Participant).delete()
        self._db.session.query(ShareHolding).delete()
        self._db.session.commit()

    def SetUpDatabase(self):
        pass
