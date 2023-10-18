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
        try:
          message = b_message.decode()
          #response = ''
          response = self.Data.feed(message)
          #b_response = response.encode('utf8')
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
    else:
      socket.close()

logger.add('/var/log/Data_log/Interaction_event.log', filter = lambda record: 'Interaction' in record['extra'])
Interaction_event_log = logger.bind(Interaction = True)
Interaction_event_log.info('Start Data Interaction event logging')

logger.add('/var/log/Data_log/Interaction_error.log', filter = lambda record: 'Interaction' in record['extra'])
Interaction_error_log = logger.bind(Interaction = True)
Interaction_error_log.error('Start Data Interaction error logging')

logger.add(sink='/var/log/Data_log/ZMQ_event.log', rotation="1 day", retention="1 week", compression="bz2" , format="{time} {level} {extra[ip]} {message}", filter = lambda record: 'ZMQ' in record['extra'])
ZMQ_event_log = logger.bind(ZMQ=True)
ZMQ_event_log.info('Start Data ZMQ event logging')

logger.add(sink='/var/log/Data_log/ZMQ_error.log', rotation="1 day", retention="1 week", compression="bz2", format="{time} {level} {extra[ip]} {message}", filter = lambda record: 'ZMQ' in record['extra'] )
ZMQ_error_log = logger.bind(ZMQ = True)
ZMQ_error_log.error('Start Data ZMQ error logging')

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://10.68.171.111:5309")

