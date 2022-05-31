from flask import Flask
from pymongo.mongo_client import MongoClient

from api.config import DB_NAME, MONGO_URL


app = Flask(__name__)

db_client = MongoClient(MONGO_URL)

db = db_client[DB_NAME]


@app.route("/check")
def check_app():
    return {"msg": "OK!"}


@app.route("/collection-names")
def get_collection_names():
    return {"collections": db.list_collection_names()}
