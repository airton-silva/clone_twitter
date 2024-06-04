from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy()
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)


from app.controllers import default