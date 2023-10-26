#!/bin/env python3

#import psycopg2 as pq
from loguru import logger
from class_PostgreSQL import PostgreSQL
import class_PostgreSQL
from class_Feeds import Feed, HardClass, HostObject
from class_Context import Host
from datetime import datetime, timezone
import json
import os
import sys

import functions_Data as fd

class Data(object):
  '''
  The Data class architecture has convergence in mind. Convergence is the theoretical model in which agents convergently work towards their desired state.
  Data tries to provide the requesters with all the available information that is suitable for the requesting agents.
  The agent itself works convergently towards the desired state, which is defined in the role based policies.
  This way the information provided by Data enables the agent to make the promises come true.

  Data contains information along the following lines:
  - Host data
  - Domain data
  - Role data
  The role may require Data to provide the agent with context information and information about other agents.

  Data receives a message from an agent with agent specific information, which triggers a response containing the above information from Data to the agent.
  '''

  #postgres = PostgreSQL()

  def __init__(self):
    self.postgres = PostgreSQL()
    #global objects
    fd.dict_update(objects, 'Postgres', id(self.postgres))
    print(objects)
  def provide_view(self, message): # provide the agent, dit is de aanloop, geen Data

    host_object_id = self.feed(message)

  def process_message(self, message): # provide the agent, dit is de aanloop, geen Data

    host_object_id = self.hard_classes(message)
    ''' We will create the context objects first, with convergence in mind. '''
    host_object = self.feeds_host_object(id_hard_classes)
    response = self.hard_classes(id_hard_classes)
    #write_feed = feed.hard_classes()
    #response = 'Response' + self.message
    return response

  def feed(self, message): # provide the agent

    self.feed = Feed(message)

    response = self.process_message(message)

    return host_object_id

  def hard_classes(self, message): # meer convergent hard_class_desired

    id_feed = self.feed.insert_feed()
    query = self.feed.check_exists()
    exists = self.postgres.check_exists(query)
    exists = exists[0]
    if exists:
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
    return (id_hard_classes,)

  def feeds_host_object(id_hard_classes): # host_object_desired
    query = 'select uqhost, domain from feeds.hard_classes where id = {}'.format(id_hard_classes)
    uqhost, domain = self.postgres.pool_query(query)
    self.host = Host(uqhost, domain)
    ''' Now store the Host object_id in feeds.host_objects, for later use '''
    exists = self.postgres.check_exists(query)
    return host_object

  def insert_json_feed(self, message):
    message_json = json.dumps(message)
    Data_event_log.info(message_json)
    timestamp = datetime.now(timezone.utc)
    query = "insert into feeds.json_in ( message_time, message_in ) values ( '{}', '{}' ) returning id;".format( timestamp , message_json )
    id_feed = self.postgres.pool_insert(query)
    Data_event_log.info('json_in message inserted with id {}.'.format(id_feed[0]))
    return id_feed

logger.add('/var/log/Data_log/Data_event.log', rotation="1 day", retention="1 week", compression="bz2", filter = lambda record: 'Data' in record['extra'] )
Data_event_log = logger.bind(data = True)
Data_event_log.info('Start Data Data event logging')

logger.add('/var/log/Data_log/Data_error.log', rotation="1 day", retention="1 week", compression="bz2", filter = lambda record: 'Data' in record['extra'], level="ERROR")
Data_error_log = logger.bind(error = True)
Data_error_log.info('Start Data Data ERROR logging')

