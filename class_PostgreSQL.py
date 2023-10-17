#!/bin/env python3

import psycopg2 as pq

class PostgreSQL():
  def __init__(self, db="data", user="www_data"):
    try:
      self.conn = pg.pool.ThreadedConnectionPool(3, 12, user=user, password='webhu15iio', host='10.68.171.111', port='5432', database=db )
    except (Exception, psycopg2.DatabaseError) as error:
      error_log.info("Error while connecting to PostgreSQL {}".format(error.args)

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

