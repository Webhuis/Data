#!/bin/env python3

from datetime import datetime, timezone
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
    self.cpus   = int(message_json["cpus"])
    self.arch   = message_json["arch"]

  def check_exists(self):
    query = "select exists(select 1 from feeds.hard_classes where uqhost = '{}' and domain = '{}');".format(self.uqhost, self.domain)
    return query

  def read_hard_classes(self):
    query = "select id, uqhost, domain, os, ostype, flavor, cpus, arch, timestamp from feeds.hard_classes where uqhost = '{}' and domain = '{}'".format(self.uqhost, self.domain)
    return query

  def insert_feed(self, message):
    timestamp = datetime.now(timezone.utc)
    query = "insert into feeds.hard_classes (uqhost, domain, os, ostype, flavor, cpus, arch, timestamp) values ('{}', '{}', '{}', '{}', '{}', {}, '{}', '{}') returning id, uqhost, domain;".format(self.uqhost, self.domain, self.os, self.ostype, self.flavor, self.cpus, self.arch, timestamp)
    return query

  def check_update(self, values):
    if self.cpus == values[5]:
      checked = True
    else:
      checked = False
    return checked

  def update_hard_classes(self, values):
    timestamp = datetime.now(timezone.utc)
    query = "update feeds.hard_classes set ( cpus = '{}', timestamp = '{}' ) where uqhost = '{}' and domain = '{}';".format(values[5], timestamp, self.uqhost, self.domain)
    return query

