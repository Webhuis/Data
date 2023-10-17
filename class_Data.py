#!/bin/env python3

#import psycopg2 as pq
from loguru import logger
from class_PostgreSQL import PostgreSQL
import class_PostgreSQL as pq
import os
import sys

class IterClass(type):
  def __init__(classobject, classname, baseclasses, attrs):
    pass
  def __iter__(cls):
    return iter(cls._allObjects)

class Data(object):
  _allObjects = []

  __metaclass__ = IterClass

  def __init__(self):
    self.PostgreSQL()

  def feedi(message):
    self.feed = message
    response = 'Response' + message
    return response

logger.add('/var/log/Data_log/Data_event.log', filter = lambda record: 'data' in record['extra'] )
Data_event_log = logger.bind(data = True)
Data_event_log.info('Start Data Data event logging')

logger.add('/var/log/Data_log/Data_error.log', filter = lambda record: 'error' in record['extra'] )
Data_error_log = logger.bind(error = True)
Data_error_log.info('Start Data Data error logging')

