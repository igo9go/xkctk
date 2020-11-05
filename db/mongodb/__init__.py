#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pymongo import MongoClient
from config import MONGODB_PORT, MONGODB_NAME, MONGODB_HOST

conn = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = conn[MONGODB_NAME]


class MongoCollection:
    def __init__(self, table):
        self.table = db[table]

    def get(self, **kwargs):
        return self.table.find(kwargs)

    def insert(self, key, data, check_exist=True):
        res = 'INSERT'
        if check_exist:
            if type(data) == dict:
                res = self.update_or_insert(key, data)
            else:
                if type(data) == list:
                    self.update_or_inserts(key, data)
        else:
            if type(data) == dict:
                self._insert_one(data)
            elif type(data) == list:
                self._insert_many(data)
        return res

    def update_or_insert(self, key, data):
        result = self.table.find_one({key: data[key]})
        if type(result) is dict:
            self.table.update_one({key: data[key]}, {'$set': data})
            op_result = 'UPDATE'
        else:
            self._insert_one(data)
            op_result = 'INSERT'
        return op_result

    def update_or_inserts(self, key, data):
        res = 'INSERT'
        for d in data:
            if self.update_or_insert(key, d) == 'UPDATE':
                res = 'UPDATE'
        return res

    def _insert_one(self, data):
        return self.table.insert_one(data).inserted_id

    def _insert_many(self, data):
        self.table.insert_many(data)
        return len(data)


if __name__ == '__main__':
    data = {'video_num': 0, 'pic_num': 8, 'comment_id': '643962374688604160', 'id': '6b6934a83fa4385ed4ec53f987e07b5f'}
    col = MongoCollection('爱迪斯')
    col.insert('id', data)
