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
    self.message_json = json.loads(message)
    self.pg_id_feed = self.insert_feed()
    self.hardclass = HardClass(message_json)
    return (self)

  def insert_feed(self):
    timestamp = datetime.now(timezone.utc)
    query = 'insert into feeds.json_in ( message_time, message_in ) values ( "{}", "{}" ) returning id;'.format( timestamp , self.message_json )
    print('feed.inset_query', query)
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

  def __init__(self, message):
    self.uqhost = message_json["uqhost"]
    self.domain = message_json["domain"]
    self.os     = message_json["os"]
    self.ostype = message_json["ostype"]
    self.flavor = message_json["flavor"]
    self.cpus   = int(message_json["cpus"])
    self.arch   = message_json["arch"]
    self.postgres = fd.fetch_object(fd.objects, 'Postgres')
    self.timestamp = datetime.now(timezone.utc)
    self.exists = self.exists()

    if self.exists == '1':
      query = self.update_hard_classes()
    else:
      query = self.feed.insert_hard_classes()
    uqhost, domain, id_hard_classes = self.postgres.pool_insert(query)
    Data_event_log.info('Hard_classes {} {} {}'.format(self.uqhost, self.domain, id))

    return(self)

  def check_exists(self):
    query = "select exists(select 1 from feeds.hard_classes where uqhost = '{}' and domain = '{}') return exists;".format(self.uqhost, self.domain)
    self.exists = self.postgres.pool_query(query)

  def read_hard_classes(self):
    query = "select id, uqhost, domain, os, ostype, flavor, cpus, arch, timestamp from feeds.hard_classes where uqhost = '{}' and domain = '{}'".format(self.uqhost, self.domain)
    return query

  def insert_hard_classes(self):
    query = "insert into feeds.hard_classes (uqhost, domain, os, ostype, flavor, cpus, arch, timestamp) values ('{}', '{}', '{}', '{}', '{}', {}, '{}', '{}') returning id;".format(self.uqhost, self.domain, self.os, self.ostype, self.flavor, self.cpus, self.arch, timestamp)
    return query

  def update_hard_classes(self):
    query = "update feeds.hard_classes set ( cpus = '{}', timestamp = '{}' ) where uqhost = '{}' and domain = '{}' returning id;".format(values[5], timestamp, self.uqhost, self.domain)
    return query

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

