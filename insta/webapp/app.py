from flask import Flask
from flask.ext.pymongo import PyMongo
import settings


app = Flask(__name__)
app.config['MONGO_DBNAME'] = settings.mongo_dbname
app.config['MONGO_HOST'] = settings.mongo_host
app.config['MONGO_PORT'] = settings.mongo_port
app.config['SECRET_KEY'] = settings.secret_key
mongo = PyMongo(app)
import views