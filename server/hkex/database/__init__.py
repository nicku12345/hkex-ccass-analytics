from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def DatabaseInitApp(app, db=db):
    db.init_app(app)

    from hkex.database.models.Participant import Participant
    from hkex.database.models.ShareHolding import ShareHolding

    with app.app_context():
        db.create_all()
