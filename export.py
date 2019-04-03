
import argparse
import yaml
from joiner import Joiner
from dumper import mongodump
from pymongo import MongoClient

ap = argparse.ArgumentParser()
ap.add_argument("-host", "--host", required=True, help="mongodb link (host)")
ap.add_argument("-d", "--db", required=True, help="mongodb database name")
ap.add_argument("-i", "--input", required=True, help="input yaml config file")
ap.add_argument("-p", "--path", required=True, help="path to dump")
ap.add_argument("-l", "--level", help="deep level limit", default=10)

args = vars(ap.parse_args())

db=None
dump={}
configuration=None


def fetch(name, info, data, level):
    global db,configuration
    optional_query = {}
    if "query" in info:
        optional_query = info['query']

    sort = [("_id", 1)]
    if "sort" in info:
        sort = info['sort']

    limit = 100000
    if "limit" in info:
        limit = info['limit']

    projection = None
    if name in configuration and "projection" in configuration[name]:
        projection = configuration[name]["projection"]

    required_query = {}
    if level > 0:
        joiner = Joiner(info['currentKey'], info['parentKey'], data)
        required_query = joiner.join()
        if not required_query:
            return []

    documents = db[name].find({**optional_query,**required_query},projection).sort(sort).limit(limit)
    docs = []
    for document in documents:
        docs.append(document)

    return docs


def append(name,data):
    global dump
    if name not in dump:
        dump[name] = []
    for document in data:
        dump[name].append(document['_id'])


def set_configuration():
    global configuration
    with open(args['input']) as input:
        configuration = yaml.safe_load(input)


def set_db(db_):
    global db
    db = db_


def export_recursively(name, info, data=None, level=0):
    global configuration
    if level > int(args['level']):
        return
    if level == 0 and "start" not in info:
        return
    if level > 0 and not data:
        return

    data = fetch(name, info, data, level)
    append(name,data)

    if name not in configuration:
        return
    if "relations" in configuration[name]:
        for child_name, child_info in configuration[name]['relations'].items():
            if isinstance(child_info,list):
                for i in child_info:
                    export_recursively(child_name, i, data, level + 1)
            else:
                export_recursively(child_name, child_info, data, level+1)


def export():
    for name, info in configuration.items():
        export_recursively(name, info)


def main():
    global dump
    client = MongoClient(args['host'])
    set_db(client[args['db']])
    set_configuration()
    export()
    mongodump(args['host'],args['db'],args['path'], dump)

if __name__ == '__main__':
    main()
