#!/usr/bin/env python3

from loguru import logger
from class_Data import Data
import class_Data
#import class_ZMQ
import sys
from datetime import datetime as dt
import zmq

import functions_Data as fd

class Interaction(object):

  loggers = {}
  '''
  Interaction class
  '''
  def __init__(self):
    self.Data = Data()
    self.Interaction_event = fd.fetch_object(Interaction.loggers, 'Interaction_event')
    self.Interaction_error = fd.fetch_object(Interaction.loggers, 'Interaction_error')
    self.ZMQ_event = fd.fetch_object(Interaction.loggers, 'ZMQ_event')
    self.ZMQ_error = fd.fetch_object(Interaction.loggers, 'ZMQ_error')
    self.zmq_init()

  def run(self):
    min_sec_num = 0
    min_sec = dt.now().strftime("%M:%S")
    min_sec_old = min_sec
    while True:

      try:
        b_message = self.socket.recv()
        print(type(b_message), b_message)
        try:
          message = b_message.decode()
          response = self.Data.provide_view(message) #, feed_object, fqhost_object):
          #b_response = response.encode('utf8')
          #queue.add_task(lambda: process_message(message))
          #queue.join()
          try:
            s_response = str(response[0])
            #print(type(s_response), s_response)
            #b_response = s_response.encode('utf8')
            self.socket.send_string(s_response)
            self.ZMQ_event.info(response[0])
          except Exception as e:
            self.ZMQ_error.info('Error sending message {}'.format(e.args))
          self.Data.work_after_response(response[1], response[2])
        except Exception as e:
          self.Interaction_error.info('Error creating task.{}'.format(e.args))
      except zmq.error.ZMQError as e:
        self.ZMQ_error.info('zmq.error.InterruptedSystemCall {}'.format(e.args))
        min_sec = dt.now().strftime("%M:%S")
        min_sec_num += 1
        if min_sec > 99 and min_sec == min_sec_old:
          self.socket.close()
          self.zmq_init()
          min_sec_num = 0
          min_sec = dt.now().strftime("%M:%S")
          min_sec_old = min_sec
      except Exception as e:
        self.ZMQ_error.info('Error receiving message {}'.format(e.args))
        sys.exit(1)
    else:
      self.socket.close()

  def zmq_init(self):
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.REP)
    self.socket.setsockopt(zmq.SNDTIMEO, 10000)
    self.socket.setsockopt(zmq.RCVTIMEO, 10000)
    self.socket.bind("tcp://10.68.171.111:5309")

for logname in ['Interaction_event', 'Interaction_error', 'ZMQ_event', 'ZMQ_error']:
  fd.add_logger.log = fd.add_logger(logname)
  fd.dict_update(Interaction.loggers, '{}'.format(logname), fd.add_logger.log)
