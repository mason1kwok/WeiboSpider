import time
import pymongo
import psycopg2
import settings
import face
import hashlib

from enum import IntEnum

class FaceState(IntEnum):
    Faced = 1
    NoneFaced = 2
    Incomplete = 3

client = pymongo.MongoClient(settings.MONGO_URI)
sina_db = client[settings.SINA_DB_NAME]
db = client[settings.DB_NAME]

connection_db = psycopg2.connect(settings.PSQL_DB_CONF)
connection_db.autocommit = True
psql_db = connection_db.cursor()
threshold = 0.4


def parse_img(url, img_from, from_id):
    state = FaceState.NoneFaced
    faces = face.url2faces(url)
    vids = []

    for encodings in faces:
        if len(encodings) > 0:
            query = "SELECT id FROM vectors WHERE sqrt(power(CUBE(array[{}]) <-> vec_low, 2) + power(CUBE(array[{}]) <-> vec_high, 2)) <= {} ".format(
                ','.join(str(s) for s in encodings[0][0:64]),
                ','.join(str(s) for s in encodings[0][64:128]),
                threshold,
            ) + \
                "ORDER BY sqrt(power(CUBE(array[{}]) <-> vec_low, 2) + power(CUBE(array[{}]) <-> vec_high, 2)) ASC LIMIT 1".format(
                    ','.join(str(s) for s in encodings[0][0:64]),
                    ','.join(str(s) for s in encodings[0][64:128]),
                )
            psql_db.execute(query)
            row = psql_db.fetchone()
            print("query:", row)
            if row is not None and row[0] not in vids:
                vids.append(row[0])
            elif len(faces) <= 1:
                query = "INSERT INTO vectors (file, vec_low, vec_high) VALUES ('{}', CUBE(array[{}]), CUBE(array[{}])) RETURNING id".format(
                    url,
                    ','.join(str(s) for s in encodings[0][0:64]),
                    ','.join(str(s) for s in encodings[0][64:128]),
                )
                psql_db.execute(query)
                vids.append(psql_db.fetchone()[0])
                print(query, vids)
            else:
                state = FaceState.Incomplete
    if len(vids) > 0:
        relation = {"from": img_from, "from_id": from_id}
        m = hashlib.md5()
        m.update(url.encode(encoding='utf-8'))
        url_md5 = m.hexdigest()    
        image = db["Images"].find_one({'_id': url_md5})
        if image:
            vectors = image.get("vectors", [])
            for vid in vids:
                if vid not in vectors:
                    vectors.append(vid)
            if len(vectors) > 0:
                db["Images"].update_one({'_id': url_md5}, {'$set': {'vectors': vectors, '_updated': int(time.time())}})
            if relation not in image["relations"]:
                db["Images"].update_one({'_id': url_md5}, {'$push': {'relations': relation}, '$set': {'_updated': int(time.time())}})
        else:
            image = {
                '_id': url_md5,
                'sign': url_md5,
                'url': url,
                'relations': [relation, ],
                'vectors': vids,
                '_created': int(time.time()),
                '_updated': int(time.time())
            }
            db["Images"].insert_one(image)
        if state != FaceState.Incomplete:
            state = FaceState.Faced
    return state

def parseHead():
    infos = sina_db['Information'].find({'icon':{'$ne': None}, 'face_state': None})
    while infos.count() > 0:
        for info in infos:
            url = info.get('icon')
            if url is None:
                continue
            url = url.replace(".180", "")
            print(url)
            state = parse_img(url, "SINA_INFORMATION", info.get("_id"))
            sina_db['Information'].update_one({"_id": info.get("_id")}, {'$set': {"face_state": state}})
        infos = sina_db['Information'].find({'icon':{'$ne': None}, 'face_state': None})

def parseImage():
    # for info in sina_db['Information'].find():
    #     print(info)
    tweets = sina_db['Tweets'].find({'image_url':{'$ne': None}, 'face_state': None})
    while tweets.count() > 0:
        for tweet in tweets:
            state = FaceState.NoneFaced
            for img in tweet.get('image_url', []):
                img = img.replace("wap180", "large")
                print(img)
                tmp = parse_img(img, "SINA_TWEET", tweet.get("_id"))
                if tmp == FaceState.Faced:
                    state = tmp
            sina_db['Tweets'].update_one({"_id": tweet.get("_id")}, {'$set': {"face_state": state}})
        tweets = sina_db['Tweets'].find({'image_url':{'$ne': None}, 'face_state': None})

if __name__ == "__main__":

    index = 0
    while True:
        try:
            parseHead()
            parseImage()
            index = 0
        except Exception as e:
            print(e)
            if index > 10:
                break
            time.sleep(1)
            index += 1

    if connection_db is not None:
        connection_db.close()

