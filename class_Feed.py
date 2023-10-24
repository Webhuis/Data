#!/bin/env python3

import json
import os
import sys

class IterClass(type):
  def __init__(classobject, classname, baseclasses, attrs):
    pass
  def __iter__(cls):
    return iter(cls._allObjects)

class Feed(object):
  _allObjects = []

  __metaclass__ = IterClass

  def __init__(self, message):
    message_json = json.loads(message)
    self.uqhost = message_json["uqhost"]
    self.domain = message_json["domain"]
    self.os     = message_json["os"]
    self.ostype = message_json["ostype"]
    self.flavor = message_json["flavor"]
    self.cpus   = message_json["cpus"]
    self.arch   = message_json["arch"]

  def check_exists(self):
    query = "select exists(select 1 from feeds.hard_classes where uqhost = '{}' and domain = '{}');".format(self.uqhost, self.domain)
    return query

  def read_hard_classes(self):
    query = "select uqhost, domain, os, ostype, flavor, cpus, arch from feeds.hard_classes where uqhost = '{}' and domain = '{}'".format(self.uqhost, self.domain)
    return query

  def insert_feed(self, message):
    query = "insert into feeds.hard_classes (uqhost, domain, os, ostype, flavor, cpus, arch) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(self.uqhost, self.domain, self.os, self.ostype, self.flavor, self.cpus, self.arch)
    return query

  def check_update(self, values):
    if self.cpus == values[5]:
      checked = True
    else:
      checked = False
    return checked

  def update_hard_classes(self, values):
    query = "update feeds.hard_classes set ( cpus = {} ) where uqhost = {} and domain = {};".format(values[5], self.uqhost, self.domain)
    return query

