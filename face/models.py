import constants

def find_vid(encodings, threshold):
    query = "SELECT id FROM vectors WHERE sqrt(power(CUBE(array[{}]) <-> vec_low, 2) + power(CUBE(array[{}]) <-> vec_high, 2)) <= {} ".format(
        ','.join(str(s) for s in encodings[0][0:64]),
        ','.join(str(s) for s in encodings[0][64:128]),
        threshold,
    ) + \
        "ORDER BY sqrt(power(CUBE(array[{}]) <-> vec_low, 2) + power(CUBE(array[{}]) <-> vec_high, 2)) ASC LIMIT 1".format(
            ','.join(str(s) for s in encodings[0][0:64]),
            ','.join(str(s) for s in encodings[0][64:128]),
    )
    print(query)
    constants.psql_db.execute(query)
    row = constants.psql_db.fetchone()
    if row is not None:
        return row[0]
    else:
        return None


def find_image(vid):
    return constants.db["Images"].find({"vectors": vid}).limit(10)

def find_sina(from_type, from_id):
    if from_type == "SINA_TWEET":
        return constants.sina_db["Tweets"].find({"_id": from_id})
    elif from_type == "SINA_INFORMATION":
        return constants.sina_db["INFOMATION"].find({"_id": from_id})
    