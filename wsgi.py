# pylint: disable=missing-docstring

from flask import Flask
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from models import Product

migrate = Migrate(app, db)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World!", 200