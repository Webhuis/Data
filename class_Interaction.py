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

  def run(self):
    #self.Interaction_error = fd.fetch_object(fd.objects, 'Interaction_error')
    #self.ZMQ_error = fd.fetch_object(fd.objects, 'ZMQ_error')
    while True:
      try:
        b_message = socket.recv()
        try:
          message = b_message.decode()
          response = self.Data.provide_view(message)
          print(response)
          #b_response = response.encode('utf8')
          #queue.add_task(lambda: process_message(message))
          #queue.join()
          try:
            s_response = str(response[0])
            #print(type(s_response), s_response)
            #b_response = s_response.encode('utf8')
            socket.send_string(s_response)
            Interaction.ZMQ_event.info(response)
          except Exception as e:
            Interaction.self.ZMQ_error.info('Error sending message {}'.format(e.args))
        except Exception as e:
          Interaction.Interaction_error.info('Error creating task.{}'.format(e.args))
      except Exception as e:
        Interaction.ZMQ_error.info('Error receiving message {}'.format(e.args))
        sys.exit(1)
    else:
      socket.close()

for logname in ['Interaction_event', 'Interaction_error', 'ZMQ_event', 'ZMQ_error']:
  log = fd.add_logger(logname)
  print(self.log, type(self.log), id(self.log))
  self.log.info ('Start logging {}.'.format(logname))
  fd.dict_update(Interaction.loggers, '{}'.format(logname), self.log)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://10.68.171.111:5309")
