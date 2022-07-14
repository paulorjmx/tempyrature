import logging
from pymongo.mongo_client import MongoClient
from confluent_kafka import Consumer

from api.config import DB_NAME, MONGO_URL


logger = logging.getLogger("processor")

c = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'counting-group',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
})
c.subscribe(['city_temp'])

db_client = MongoClient(MONGO_URL)
db = db_client[DB_NAME]
db_city = db["cities"]


def main():
    while True:
        msg = c.poll(1.0)

        if msg is None:
            continue
        elif not msg.error():
            s = msg.value().decode("utf-8")
            logger.debug(s)
            city, temp = s.split()

            if db_city.find_one({"city": city}):
                db_city.update_one({"city": city}, {"temp": temp})
            else:
                db_city.insert_one({"city": city, "temp": temp})                


if __name__ == '__main__':
    logger.info("processor started")
    main()
