from flask import Flask
from flask_cors import CORS
from datetime import timedelta
from datetime import datetime
from flask_pymongo import PyMongo
from bson import ObjectId
from app.clases.fixManager import fixManager
import logging
import time
import redis
#logging.basicConfig(filename=f'reportsBots.log', level=logging.INFO,
 #                   format='%(asctime)s %(name)s  %(levelname)s  %(message)s  %(lineno)d ')
log = logging.getLogger(__name__)
   
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/rofex'
mongo = PyMongo(app)
sesionesFix = {}
fixM = fixManager()
urlAppFix = "http://127.0.0.1:5000"
redis_cliente = redis.StrictRedis(host='localhost', port=6379, db=0)
from app.requests import *

