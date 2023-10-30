#!/bin/env python3

from datetime import datetime, timezone
import json
import os
import sys

import functions_Data as fd

class Feed(object):

  def __init__(self, message):
    self.message = message
    self.postgres = fd.fetch_object(fd.objects, 'Postgres')
    self.pg_id_feed = self.insert_feed()
    self.message_json = json.loads(message)
    self.hardclass = HardClass(self.message_json)
    return (self)

  def insert_feed(self):
    timestamp = datetime.now(timezone.utc)
    query = "insert into feeds.json_in ( message_time, message_in ) values ( '{}', '{}' ) returning id;".format( timestamp , self.message )
    id = self.postgres.pool_insert(query)
    return id

  def update_feed(self):
    timestamp = datetime.now(timezone.utc)
    query = "insert into feeds.json_in ( message_time, message_in ) values ( '{}', '{}' ) returning id;".format( timestamp , message_json )
    return query

  def delete_feed(self):
    timestamp = datetime.now(timezone.utc)
    query = "insert into feeds.json_in ( message_time, message_in ) values ( '{}', '{}' ) returning id;".format( timestamp , message_json )
    return query

class HardClass(object):

  def __init__(self, message_json):
    self.uqhost = message_json["uqhost"]
    self.domain = message_json["domain"]
    self.os     = message_json["os"]
    self.ostype = message_json["ostype"]
    self.flavor = message_json["flavor"]
    self.cpus   = int(message_json["cpus"])
    self.arch   = message_json["arch"]
    self.postgres = fd.fetch_object(fd.objects, 'Postgres')
    self.timestamp = datetime.now(timezone.utc)
    self.exists = self.check_exists()
    print(self.exists)
    if self.exists == True:
      self.query = self.update_hard_classes()
      self.id_hardclass = self.postgres.pool_update(query)
    else:
      self.query = self.insert_hard_classes()
      self.id_hardclass = self.postgres.pool_insert(query)
    print(self.id_hardclass)
    Data_event_log.info('Hard_classes {} {} {}'.format(self.uqhost, self.domain, id))

    return(self)

  def check_exists(self):
    query = "select exists(select 1 from feeds.hard_classes where uqhost = '{}' and domain = '{}');".format(self.uqhost, self.domain)
    exists = self.postgres.pool_query(query)
    return exists[0][0]

  def read_hard_classes(self):
    query = "select id, uqhost, domain, os, ostype, flavor, cpus, arch, timestamp from feeds.hard_classes where uqhost = '{}' and domain = '{}'".format(self.uqhost, self.domain)
    return query

  def insert_hard_classes(self):
    self.query = "insert into feeds.hard_classes (uqhost, domain, os, ostype, flavor, cpus, arch, timestamp) values ('{}', '{}', '{}', '{}', '{}', {}, '{}', '{}') returning id;".format(self.uqhost, self.domain, self.os, self.ostype, self.flavor, self.cpus, self.arch, self.timestamp)
    print(self.query)
    return self.query

  def update_hard_classes(self):
    self.query = "update feeds.hard_classes set ( cpus = '{}', timestamp = '{}' ) where uqhost = '{}' and domain = '{}' returning id;".format(values[5], self.timestamp, self.uqhost, self.domain)
    print(self.query)
    return self.query

class HostObject(object):

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

