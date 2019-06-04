import pymongo
import psycopg2
import settings
import face
import hashlib

client = pymongo.MongoClient(settings.LOCAL_MONGO_HOST, settings.LOCAL_MONGO_PORT)
sina_db = client[settings.SINA_DB_NAME]
db = client[settings.DB_NAME]

connection_db = psycopg2.connect(settings.PSQL_DB_CONF)
psql_db = connection_db.cursor()


def parse_img(url, img_from, from_id):
    url_md5 = hashlib.md5().update(url.encode(encoding='utf-8')).hexdigest()
    image = db["Images"].find_one({'_id': url_md5})
    if image:
        pass
    else:
        encodings = face.url2faces(url)
        if not encodings.any():
            return
        
        query = "INSERT INTO vectors (file, vec_low, vec_high) VALUES ('{}', CUBE(array[{}]), CUBE(array[{}]))".format(
            url,
            ','.join(str(s) for s in encodings[0][0:64]),
            ','.join(str(s) for s in encodings[0][64:128]),
        )
        psql_db.execute(query)


if __name__ == "__main__":

    for info in sina_db['Information'].find():
        print(info)

    for tweet in sina_db['Tweets'].find({'image_url':{'$ne': None}}).sort('crawl_time', -1).limit(100):
        for img in tweet.get('image_url', []):
            print(img)
            print(face.url2faces(img))


