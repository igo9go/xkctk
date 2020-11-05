#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib


def hash_string(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
        hash = hashlib.md5()
        hash.update(data)
        return hash.hexdigest()
