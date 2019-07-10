import pymongo
import psycopg2
import settings

from enum import IntEnum


class FaceState(IntEnum):
    Faced = 1
    NoneFaced = 2

client = pymongo.MongoClient(settings.MONGO_URI)
sina_db = client[settings.SINA_DB_NAME]
db = client[settings.DB_NAME]

connection_db = psycopg2.connect(settings.PSQL_DB_CONF)
connection_db.autocommit = True
psql_db = connection_db.cursor()
threshold = 0.4
