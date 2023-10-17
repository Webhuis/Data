#!/usr/bin/env python3

from loguru import logger
from class_Data import Data
import class_Data
#import class_ZMQ
import sys
import zmq

class Interaction(object):
  '''
  Interaction class
  '''

  def __init__(self):
    self.Data = Data()

  def run(self):
    while True:
      try:
        b_message = socket.recv()
        message = b_message.decode()
        try:
          response = self.Data.feed(message)
          #queue.add_task(lambda: process_message(message))
          #queue.join()
          try:
            socket.send_string(response)
          except Exception as e:
            ZMQ_error_log.info('Error sending message {}'.format(e.args))
        except Exception as e:
          Interaction_error_log.info('Error creating task.{}'.format(e.args))
      except Exception as e:
        ZMQ_error_log.info('Error receiving message {}'.format(e.args))
        sys.exit(1)
      finally:
        socket.close()

logger.add('/var/log/Data_log/Interaction_event.log', filter = lambda record: 'data' in record['extra'] )
Interaction_event_log = logger.bind(data = True)
Interaction_event_log.info('Start Data Interaction event logging')

logger.add('/var/log/Data_log/Interaction_error.log', filter = lambda record: 'error' in record['extra'] )
Interaction_error_log = logger.bind(error = True)
Interaction_error_log.info('Start Data Interaction error logging')

logger.add('/var/log/Data_log/ZMQ_event.log', filter = lambda record: 'data' in record['extra'] )
ZMQ_event_log = logger.bind(data = True)
ZMQ_event_log.info('Start Data ZMQ event logging')

logger.add('/var/log/Data_log/ZMQ_error.log', filter = lambda record: 'error' in record['extra'] )
ZMQ_error_log = logger.bind(error = True)
ZMQ_error_log.info('Start Data ZMQ error logging')

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://10.68.171.111:5309")

