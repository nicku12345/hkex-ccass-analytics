import logging
from hkex.database import db


class BaseRepository:

    def __init__(self):
        self._db = db
        self._logger = logging.getLogger("flask.app")

    def Save(self):
        self._db.session.commit()

    def AddAndSave(self, objs):
        self._db.session.bulk_save_objects(objs)
        self.Save()
