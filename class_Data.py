#!/bin/env python3

#import psycopg2 as pq
from loguru import logger
from class_PostgreSQL import PostgreSQL
import class_PostgreSQL
from class_Feeds import Feed, HardClass
from class_Context import FQHost, Domain, Role
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

  loggers = {}

  def __init__(self):
    self.postgres = PostgreSQL()
    self.Data_event = fd.fetch_object(Data.loggers, 'Data_event')
    self.Data_error = fd.fetch_object(Data.loggers, 'Data_error')

  def provide_view(self, message): # provide the agent, dit is de aanloop, geen Data

    self.feed, self.uqhost, self.domain = self.feed_to_hardclass(message, self.postgres)
    self.fqhost_object = FQHost(self.uqhost, self.domain)
    self.Data_event.info('Actual FQHost {} in database Data.'.format(self.fqhost_object))
    response = self.fqhost_object
    return response

  def process_message(self, message): # provide the agent, dit is de aanloop, geen Data

    host_object_id = self.hard_classes(message)
    ''' We will create the context objects first, with convergence in mind. '''
    host_object = self.feeds_host_object(id_hard_classes)
    response = self.hard_classes(id_hard_classes)
    #write_feed = feed.hard_classes()
    #response = 'Response' + self.message
    return response

  def feed_to_hardclass(self, message, postgres):

    self.feed = Feed(message, postgres)
    self.id_feed = self.feed.insert_feed()

    self.hardclass = HardClass(message, postgres)
    self.uqhost, self.domain = self.hardclass.set_hardclass()

    self.Data_event.info('Actual feed and fqdn hardclasses {} {} {} in database Data.'.format(self.id_feed, self.uqhost, self.domain))

    return (self.id_feed, self.uqhost, self.domain)

  def feeds_host_object(id_hard_classes): # host_object_desired
    query = 'select uqhost, domain from feeds.hard_classes where id = {}'.format(id_hard_classes)
    uqhost, domain = self.postgres.pool_query(query)
    self.host = Host(uqhost, domain)
    ''' Now store the Host object_id in feeds.host_objects, for later use '''
    exists = self.postgres.check_exists(query)
    return host_object

for logname in ['Data_event', 'Data_error']:
  fd.add_logger.log = fd.add_logger(logname)
  fd.dict_update(Data.loggers, '{}'.format(logname), fd.add_logger.log)

