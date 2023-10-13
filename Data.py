#!/usr/bin/env python3

import subprocess as sp
from threading import Thread   # currentThread is not used
import multiprocessing as mp
import loguru as log
import os
import time as tm
import datetime as dt
import sys
import zmq

import classes_Data as d
import classes_Data as pg
import classes_feeds as f
import classes_Taskqueue as t

'''
Data is an Object oriented program
https://wiki.webhuis.nl/Data
'''
'''
Start logging first
'''

log.logger.add('error.log', filter = lambda record: 'error' in record['extra'] )
error_log = log.logger.bind(error = True)
log.logger.add('Data.log', filter = lambda record: 'Data' in record['extra'] )
Data_log = log.logger.bind(Data = True)
log.logger.add('data_messages.log', filter = lambda record: 'Data' in record['extra'] )
data_messages_log = log.logger.bind(veres = True)

'''
Connect to the Data database
'''

tcpl = pg.Data()

'''
Start de Taskqueue
'''

num_worker_threads = 4
pool = mp.Pool(processes=4)
queue_manager = mp.Manager()
queue = t.TaskQueue()

'''
Start de message queue
'''
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://10.68.171.111:5309")

def main():

  '''
  CFEngine start this program daemonised mode
  1. Initialise the host_objects for the run
  2. Start the Task queue
  '''

  while True:
    try:
      message = socket.recv()
      try:
        queue.add_task(lambda: process_message(message))
        queue.join()
        try:
          socket.send_string(response)
        except Exception as e:
          data_messages_log.info('Error sending message {}'.format(e.args))
      except Exception as e:
        data_messages_log.info('Error creating task.{}'.format(e.args))
    except Exception as e:
      data_messages_log.info('Error receiving message {}'.format(e.args))

  socket.close()
  data_messages_log.close()
  Data_log.close()
  error_log.close()

def process_message(message):

  timestamp = datetime.datetime.now()
  message_feed = f.Feed(timestamp, message)
  message_object = id(message_feed)
  data_messages_log.info('message_feed')

'''
    if received:
      message_object = create_feed_object(message)
      response = 'Message processed' + '\n'
      b_response = message.encode('utf8')
      try:
        socket.send_string(response)
        data_messages_log.info('Sending {}.'.format(response))
      except Exception as e:
        data_messages_log.info('Error sending message {}'.format(e.args))
'''

def create_feed_object(message):
  message = b_message.decode()
  return message_object

def add_feed_queue(message):
  data_messages_log.info('Receiving {}.'.format(message))
  data_messages_log.info('Sending {}.'.format(response))
  message = b_message.decode()

  queue.add_task(message)
  queue.join()
  return response

main()
