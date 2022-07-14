import random
from flask import Flask
from pymongo.mongo_client import MongoClient

from api.config import DB_NAME, MONGO_URL


app = Flask(__name__)

db_client = MongoClient(MONGO_URL)
db = db_client[DB_NAME]
db_city = db["cities"]


@app.route("/check")
def check_app():
    return {"msg": "OK!"}


@app.route("/collection-names")
def get_collection_names():
    return {"collections": db.list_collection_names()}


@app.route("/temp")
def get_temp(temperature: int):
    min_d = 100000
    possible_choices = []
    for c in db_city.find():
        diff = abs(temperature - c["temp"])
        if min_d >= diff:
            min_d = abs(temperature - c["temp"])
            possible_choices.append(c)
    
    return random.choice(possible_choices)
