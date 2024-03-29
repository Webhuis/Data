#!/usr/bin/env python3

from loguru import logger
import json
import sys

def fetch_object(obj_dict, obj_key):

  object = obj_dict[obj_key][0]

  return object

def dict_update(dict, key, value):

  try:
    dict[key].append(value)
  except:
    dict[key] = [value]

def make_filter(logname):
  def filter(record):
    return record['extra'].get('task') == logname
  return filter

def add_logger(logname):
  try:
    logger.add(sink='/var/log/Data_log/' + logname + '.log', filter=make_filter(logname), rotation='1 day', retention='1 week', compression='bz2')
  except Exception as e:
    print('logger.add gaat fout', e.args)
  try:
    log = logger.bind(task='{}'.format(logname))
    #dict_update(objects, '{}'.format(logname), log)
  except Exception as e:
    print('logger.bind gaat fout', e.args)
  try:
    log.info('Start logging {}'.format(logname))
  except Exception as e:
    print('log.info gaat fout', e.args)
  return log

def to_json(j_dict, containers):

  json_object = { '{}'.format(j_dict): []}
  for container in containers:
    json_object[j_dict].append(container)

  return json_object

objects = {}
