
from bson import ObjectId
import os


def stringify(ids):
    res = []
    for id in ids:
        res.append('{"$oid":"' + str(id) + '"}')
    return ",".join(res)


def query(ids):
    return '\'{"_id":{"$in":[' + stringify(ids) + ']}}\''


def process(host, db, collection, path, ids):
    os.system(" ".join(
        ["mongodump", "--host", host, '--db', db, '--collection', collection, '-q', query(ids), "--out", path]))


def mongodump(host, db, path, data):
    for name, val in data.items():
        ids = set(val)
        if len(ids):
            process(host, db, name, path, ids)
