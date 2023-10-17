#!/usr/bin/env python3

from loguru import logger
from class_Data import Data
import class_Data
#import class_ZMQ
import zmq

class Interaction(object):
  '''
  Interaction class
  '''

  def __init__(self):
    self.Data = Data()
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.REP)
    self.socket.bind("tcp://10.68.171.111:5309")
    logger.add('/var/log/Data_log/ZMQ_event.log', filter = lambda record: 'data' in record['extra'] )
    self.ZMQ_event_log = logger.bind(data = True)
    self.ZMQ_event_log.info('Start Data ZMQ event logging')

    logger.add('/var/log/Data_log/ZMQ_error.log', filter = lambda record: 'error' in record['extra'] )
    self.ZMQ_error_log = logger.bind(error = True)
    self.ZMQ_error_log.info('Start Data ZMQ error logging')

  def run(self):
    while True:
      try:
        message = self.socket.recv()
        try:
          response = self.Data.feed(message)
          #queue.add_task(lambda: process_message(message))
          #queue.join()
          try:
            self.socket.send_string(response)
          except Exception as e:
            self.ZMQ_error_log.info('Error sending message {}'.format(e.args))
        except Exception as e:
          self.Interaction_log.info('Error creating task.{}'.format(e.args))
      except Exception as e:
        self.ZMQ_error_log.info('Error receiving message {}'.format(e.args))
      finally:
        self.socket.close()

logger.add('/var/log/Data_log/Interaction_event.log', filter = lambda record: 'data' in record['extra'] )
Interaction_event_log = logger.bind(data = True)
Interaction_event_log.info('Start Data Interaction event logging')

logger.add('/var/log/Data_log/Interaction_error.log', filter = lambda record: 'error' in record['extra'] )
Interaction_error_log = logger.bind(error = True)
Interaction_error_log.info('Start Data Interaction error logging')

