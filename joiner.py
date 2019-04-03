
import re
from bson import ObjectId

class Joiner:

    data = None
    current_key = None
    parent_key = None

    def __init__(self, current_key, parent_key, parent_data):
        self.parent_data = parent_data
        self.current_key = current_key
        self.parent_key = parent_key

    def parse(self, type, value):
        if type == 'string':
            return str(value)
        if type == 'number':
            return int(value)
        if type == 'ObjectId':
            return ObjectId(value)
        return value

    def get_key(self, type):
        match = re.match(r'([^:]+)(:.*)?', type)
        return match.groups()[0]

    def get_type(self, type):
        match = re.match(r'([^:]+):\[?([\w]+)\]?', type)
        if match:
            return match.groups()[1]
        return None

    def get_values(self, obj, key_):
        val = []
        res = obj
        spl = key_.split('.')
        for key in spl:
            if key not in res:
                return []
            if isinstance(res[key], list):
                for item in res[key]:
                    if isinstance(item, dict) and not ObjectId.is_valid(item):
                        val += self.get_values(item, key_.split('.',1)[1])
                    else:
                        val.append(item)
                return val
            if isinstance(res[key], dict) and not ObjectId.is_valid(res[key]):
                res = res[key]
            else:
                return [res[key]]
        return val


    def join(self):
        values = []
        p_key = self.get_key(self.parent_key)
        c_key = self.get_key(self.current_key)
        c_type = self.get_type(self.current_key)

        for data in self.parent_data:
            values += self.get_values(data,p_key)

        if len(values) == 0:
            return False

        parsed = []
        for value in values:
            parsed.append(self.parse(c_type, value))
        return {c_key: {"$in": parsed}}