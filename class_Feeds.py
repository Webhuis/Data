#!/bin/env python3

from datetime import datetime, timezone
import json
import os
import sys

import functions_Data as fd

class Feed(object):

  def __init__(self, message):
    self.message = message
    self.postgres = fd.fetch_objects(fd.objects, 'Postgres')
    self.pg_id_feed = self.insert_feed()
    message_json = json.loads(message)
    self.host_object_id = HardClass(message_json)
    #(id, uqhost, domain) = self.hardclass.insert_feed
    return (self.host_object_id

  def insert_feed(self):
    timestamp = datetime.now(timezone.utc)
    query = "insert into feeds.json_in ( message_time, message_in ) values ( '{}', '{}' ) returning id;".format( timestamp , self.message_json )
    self.postgres.pool_insert(query)
    return pg_id_feed

  def update_feed(self):
    timestamp = datetime.now(timezone.utc)
    query = "insert into feeds.json_in ( message_time, message_in ) values ( '{}', '{}' ) returning id;".format( timestamp , message_json )
    return query

  def delete_feed(self):
    timestamp = datetime.now(timezone.utc)
    query = "insert into feeds.json_in ( message_time, message_in ) values ( '{}', '{}' ) returning id;".format( timestamp , message_json )
    return query

class HardClass(object):

  def __init__(self, message):
    self.uqhost = message_json["uqhost"]
    self.domain = message_json["domain"]
    self.os     = message_json["os"]
    self.ostype = message_json["ostype"]
    self.flavor = message_json["flavor"]
    self.cpus   = int(message_json["cpus"])
    self.arch   = message_json["arch"]
    self.postgres = fd.fetch_objects(fd.objects, 'Postgres')
    self.postgres.pool_query(query)

    if self.exists():
      query = self.feed.read_hard_classes()
      values = self.postgres.pool_query(query)
      id_hard_classes = values[0][0]
      checked = self.feed.check_update(values[0])
      if checked:
        Data_event_log.info('Already up to date'.format(values[0][1], values[0][2]))
      else:
        query = self.feed.update_hard_classes(values[0])
        timestamp = self.postgres.pool_update(query)
        Data_event_log.info('Updated hard_classes {} {} {}'.format(values[0][0], values[0][1], timestamp))
    else:
      query = self.feed.insert_feed(message)
      uqhost, domain, id_hard_classes = self.postgres.pool_insert(query)
      Data_event_log.info('Inserted hard_classes {} {} {}'.format(uqhost, domain, id_hard_classes))
    del(self.feed)

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
    if self.cpus == values[6]:
      checked = True
    else:
      checked = False
    return checked

  def update_hard_classes(self, values):
    timestamp = datetime.now(timezone.utc)
    query = "update feeds.hard_classes set ( cpus = '{}', timestamp = '{}' ) where uqhost = '{}' and domain = '{}';".format(values[5], timestamp, self.uqhost, self.domain)
    return query

class HostObject(object):
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

