#!/usr/bin/env python3

import re
import sys

def fetch_object(obj_dict, obj_key):

    object = obj_dict[obj_key][0]

    return object

def dict_update(dict, key, value):

    try:
        dict[key].append(value)
    except:
        dict[key] = [value]

global objects
