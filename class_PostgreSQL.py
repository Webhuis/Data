#!/bin/env python3

from loguru import logger
import psycopg2 as pg
from psycopg2 import pool

class PostgreSQL():
  def __init__(self, db="data", user="www_data"):
    try:
      self.conn = pg.pool.ThreadedConnectionPool(3, 12, user=user, password='webhu15iio', host='10.68.171.50', port='5432', database=db )
      PostgreSQL_event_log.info('Start Data PostgreSQL __init__')
    except (Exception, pg.DatabaseError) as error:
      PostgreSQL_error_log.info("Error while connecting to PostgreSQL {}".format(error.args))

  def pool_query(self, query):
    try:
      pg_conn = data.pg_pool.getconn()
      pg_cursor = pg_conn.cursor()
      pg_cursor.execute(query)
      result = pg_cursor.fetchall()
    except (Exception, pg.DatabaseError) as error:
      print("Error while selecting from PostgreSQL {}".format(error.args))

    return result

  def pool_connect(self, cursor):
    self.getconn()

  def cursor(self, cursor):
    self.cur.execute(query)

  def query(self, query):
    self.cur.execute(query)

  def close(self):
    self.cur.close()
    self.conn.close()

logger.add('/var/log/Data_log/PostgreSQL_event.log', filter = lambda record: 'data' in record['extra'] )
PostgreSQL_event_log = logger.bind(data = True)
PostgreSQL_event_log.info('Start Data PostgreSQL event logging')

logger.add('/var/log/Data_log/PostgreSQL_error.log', filter = lambda record: 'error' in record['extra'] )
PostgreSQL_error_log = logger.bind(error = True)
PostgreSQL_error_log.info('Start Data PostgreSQL error logging')

