#!/usr/bin/env python3

from loguru import logger
from class_Data import Data
import class_Data
#import class_ZMQ
import sys
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

  def run(self):
    while True:
      try:
        b_message = socket.recv()
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
            socket.send_string(s_response)
            self.ZMQ_event.info(response[0])
          except Exception as e:
            self.ZMQ_error.info('Error sending message {}'.format(e.args))
          self.Data.work_after_response(response[1], response[2])
        except Exception as e:
          self.Interaction_error.info('Error creating task.{}'.format(e.args))
      except Exception as e:
        self.ZMQ_error.info('Error receiving message {}'.format(e.args))
        sys.exit(1)
    else:
      socket.close()

for logname in ['Interaction_event', 'Interaction_error', 'ZMQ_event', 'ZMQ_error']:
  fd.add_logger.log = fd.add_logger(logname)
  fd.dict_update(Interaction.loggers, '{}'.format(logname), fd.add_logger.log)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.setsockopt(zmq.SNDTIMEO, 10000)
socket.setsockopt(zmq.RCVTIMEO, 10000)
socket.bind("tcp://10.68.171.111:5309")
