import argparse
import yaml
from joiner import Joiner
from dumper import mongodump
from pymongo import MongoClient

ap = argparse.ArgumentParser()
ap.add_argument("-host", "--host", required=True, help="Mongodb link (host)")
ap.add_argument("-d", "--db", required=True, help="Mongodb database name")
ap.add_argument("-i", "--input", required=True, help="Input yaml config file")
ap.add_argument("-p", "--path", required=True, help="Path to dump")
ap.add_argument("-l", "--level", help="Database process deep level", default=10)
args = vars(ap.parse_args())


def fetch_documents(db, collection, configuration, parent_documents=None):
    optional_query = {}
    if "query" in configuration:
        optional_query = configuration['query']

    sort = [("_id", 1)]
    if "sort" in configuration:
        sort = configuration['sort']

    limit = 100000
    if "limit" in configuration:
        limit = configuration['limit']

    projection = None
    if "projection" in configuration:
        projection = configuration["projection"]

    required_query = {}

    if 'currentKey' in configuration and 'parentKey' in configuration:
        required_query = Joiner(configuration['currentKey'], configuration['parentKey'], parent_documents).join() or {}

    cursor = db[collection].find({**required_query, **optional_query}, projection).sort(sort).limit(limit)
    documents = []
    for document in cursor:
        documents.append(document)
    return documents


def append_collections_ids(collections_ids, collection, documents):
    if collection not in collections_ids:
        collections_ids[collection] = []
    for data in documents:
        collections_ids[collection].append(data['_id'])


def load_configurations():
    with open(args['input']) as input:
        configurations = yaml.safe_load(input)
    return configurations


def export_recursively(db, collection, configurations, collections_ids, documents=None, level=0, keys=None):
    if keys is None:
        keys = {}
    configuration = {}
    if collection in configurations:
        configuration = configurations[collection]

    if level > int(args['level']):
        return
    if level == 0 and "start" not in configuration:
        return

    # Append current collections
    documents = fetch_documents(db, collection, {**configuration, **keys}, documents)
    append_collections_ids(collections_ids, collection, documents)

    # Append child collections
    if collection not in configurations:
        return
    if "relations" in configuration:
        for child_collection, child_configuration in configuration['relations'].items():
            if isinstance(child_configuration, list):
                for child_configuration_i in child_configuration:
                    export_recursively(db, child_collection, configurations, collections_ids, documents, level + 1,
                                       child_configuration_i)
            else:
                export_recursively(db, child_collection, configurations, collections_ids, documents, level + 1,
                               child_configuration)


def export_queries(db, configurations):
    collections_ids = {}
    for collection, configuration in configurations.items():
        export_recursively(db, collection, configurations, collections_ids)
    return collections_ids


def main():
    # Database connection
    client = MongoClient(args['host'])
    db = client[args['db']]

    # Read Yaml Configuration
    configurations = load_configurations()

    # Exporting Database queries
    collections_ids = export_queries(db, configurations)

    # Mongodump
    mongodump(args['host'], args['db'], args['path'], collections_ids)


if __name__ == '__main__':
    main()
