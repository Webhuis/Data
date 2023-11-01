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

    self.id_feed, self.uqhost, self.domain_name = self.feed_to_hardclass(message, self.postgres)
    self.fqhost_object = FQHost(self.uqhost, self.domain_name, self.postgres)
    try:
      self.fqhost_role_view = self.get_fqhost_role_view()
      response = json.dumps(self.fqhost_role_view)
      return response
    except Execption as e:
      self.Data_error.info('Generating response failed, {}.'.format(x.args))
    finally:
      self.fqhost_object.update_fqhost()
      self.id_response = self.feed.insert_response(response)
      self.Data_event.info('Actual FQHost {} in database Data.'.format(self.fqhost_role_view))

  def get_fqhost_role_view():

    self.fqhost_role_view = self.fqhost_object.get_fqhost_role_view()
    return self.fqhost_role_view

  def feed_to_hardclass(self, message, postgres):

    self.feed = Feed(message, postgres)
    self.id_feed = self.feed.insert_feed()

    self.hardclass = HardClass(message, postgres)
    self.uqhost, self.domain = self.hardclass.set_hardclass()

    self.Data_event.info('Actual feed and fqdn hardclasses {} {} {} in database Data.'.format(self.id_feed, self.uqhost, self.domain))

    return (self.id_feed, self.uqhost, self.domain)

  def process_message(self, message): # provide the agent, dit is de aanloop, geen Data

    host_object_id = self.hard_classes(message)
    ''' We will create the context objects first, with convergence in mind. '''
    host_object = self.feeds_host_object(id_hard_classes)
    #response = json.dumps(self.hard_classes(id_hard_classes))
    response = json.dumps(['Dit is een heel verhaal als response', 'vers twee'])
    #write_feed = feed.hard_classes()
    print(response)
    return response

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

