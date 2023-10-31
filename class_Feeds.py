#!/bin/env python3

from datetime import datetime, timezone
import json
import os
import sys

import functions_Data as fd

class Feed(object):

  def __init__(self, message, postgres):
    self.message = message
    self.postgres = postgres
    self.pg_id_feed = self.insert_feed()
    self.message_json = json.loads(message)
    self.hardclass = HardClass(self.message_json, self.postgres)
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

  def __init__(self, message_json, postgres):
    self.uqhost = message_json["uqhost"]
    self.domain = message_json["domain"]
    self.os     = message_json["os"]
    self.ostype = message_json["ostype"]
    self.flavor = message_json["flavor"]
    self.cpus   = int(message_json["cpus"])
    self.arch   = message_json["arch"]
    self.timestamp = datetime.now(timezone.utc)
    self.postgres = postgres
    self.exists = self.check_exists()
    if self.exists == True:
      self.query = self.update_hard_classes()
      self.id_hardclass = self.postgres.pool_update(self.query)
    else:
      self.query = self.insert_hard_classes()
      self.id_hardclass = self.postgres.pool_insert(self.query)
    Data_event.info('Hard_classes {} {} {}'.format(self.uqhost, self.domain, id))

    return(self)

  def check_exists(self):
    query = "select exists(select 1 from feeds.hard_classes where uqhost = '{}' and domain = '{}');".format(self.uqhost, self.domain)
    exists = self.postgres.pool_query(query)
    return exists[0][0]

  def read_hard_classes(self):
    query = "select id, uqhost, domain, os, ostype, flavor, cpus, arch, timestamp from feeds.hard_classes where uqhost = '{}' and domain = '{}'".format(self.uqhost, self.domain)
    return query

  def insert_hard_classes(self):
    self.query = ("insert into feeds.hard_classes (uqhost, domain, os, ostype, flavor, cpus, arch, timestamp) "
                  "values ('{}', '{}', '{}', '{}', '{}', {}, '{}', '{}') returning id;").format(
                   self.uqhost, self.domain, self.os, self.ostype, self.flavor, self.cpus, self.arch, self.timestamp)
    return self.query

  def update_hard_classes(self):
    self.query = ("update feeds.hard_classes set os = '{}', ostype = '{}', flavor = '{}', cpus = {} , arch = '{}', timestamp = '{}' "
                  "where uqhost = '{}' and domain = '{}' returning id;").format(
                   self.os, self.ostype, self.flavor, self.cpus, self.arch, self.timestamp, self.uqhost, self.domain)
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

