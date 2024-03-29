#!/bin/env python3

from loguru import logger
import psycopg2 as pg
from psycopg2 import pool
from psycopg2.pool import ThreadedConnectionPool as ThCP
from threading import Semaphore

import functions_Data as fd

class PostgreSQL():

  loggers = {}

  def __init__(self, db="data", user="www_data"):
    self.PostgreSQL_event = fd.fetch_object(PostgreSQL.loggers, 'PostgreSQL_event')
    self.PostgreSQL_error = fd.fetch_object(PostgreSQL.loggers, 'PostgreSQL_error')
    self.pg_pool = DataThCP(8, 16, user="www_data", password='we8hu15iio', host='10.68.171.50', port='5432', database="data"
                                   , connect_timeout=9
                                   , keepalives=4
                                   , keepalives_idle=30
                                   , keepalives_interval=10
                                   , keepalives_count=5)

    self.PostgreSQL_event.info('Start Data PostgreSQL __init__')

  def db_connect(self):
    try:
      self.pg_pool = DataThCP(8, 16, user="www_data", password='we8hu15iio', host='10.68.171.50', port='5432', database="data"
                                   , connect_timeout=9
                                   , keepalives=4
                                   , keepalives_idle=30
                                   , keepalives_interval=10
                                   , keepalives_count=5)
      self.PostgreSQL_event.info('Start Data PostgreSQL db_connect.')
    except (Exception, pg.DatabaseError) as error:
      self.PostgreSQL_error.info("Error while connecting to PostgreSQL {}".format(error.args))

  def db_reconnect(self):
    try:
      self.db_closeconn()
      self.PostgreSQL_event.info('Close PostgreSQL connections')
    except (Exception, pg.DatabaseError) as error:
      self.PostgreSQL_error.info("Error while closing connections to PostgreSQL {}".format(error.args))
    self.db_connect()

  def db_closeconn(self):
    try:
      self.pg_pool.closeall()
    except (Exception, pg.DatabaseError) as error:
      self.PostgreSQL_error.info("Error while closing connections to PostgreSQL {}".format(error.args))

  def check_exists(self, query):
    try:
      pg_conn = self.pg_pool.getconn()
      pg_cursor = pg_conn.cursor()
      pg_cursor.execute(query)
      result = pg_cursor.fetchall()[0]
      pg_cursor.close()
      self.pg_pool.putconn(pg_conn)
    except (Exception, pg.DatabaseError) as error:
      result = ("Error while selecting from PostgreSQL {}".format(error.args),)
      self.PostgreSQL_error.info(result)
    return result

  def pool_query(self, query):
    try:
      pg_conn = self.pg_pool.getconn()
      pg_cursor = pg_conn.cursor()
      pg_cursor.execute(query)
      result = pg_cursor.fetchall()
      pg_cursor.close()
      self.pg_pool.putconn(pg_conn)
    except (Exception, pg.DatabaseError) as error:
      result = ("Error while selecting from PostgreSQL, time issue? {}".format(error.args),)
      print(type(result))
      self.PostgreSQL_error.info(result)
    return result

  def pool_insert(self, query):
    try:
      pg_conn = self.pg_pool.getconn()
      pg_cursor = pg_conn.cursor()
      pg_cursor.execute(query)
      pg_conn.commit()
      result = pg_cursor.fetchall()[0]
      pg_cursor.close()
      self.pg_pool.putconn(pg_conn)
      #self.PostgreSQL_event.info(result)
    except (Exception, pg.DatabaseError) as error:
      result = ("Error while inserting into PostgreSQL {}".format(error.args),)
      self.PostgreSQL_error.info(result)
    return result

  def pool_update(self, query):
    try:
      pg_conn = self.pg_pool.getconn()
      pg_cursor = pg_conn.cursor()
      pg_cursor.execute(query)
      pg_conn.commit()
      result = pg_cursor.fetchall()[0]
      pg_cursor.close()
      self.pg_pool.putconn(pg_conn)
    except (Exception, pg.DatabaseError) as error:
      result = ("Error while updating PostgreSQL {}".format(error.args),)
      self.PostgreSQL_error.info(result)
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

class DataThCP(ThCP):
  def __init__(self, minconn, maxconn, *args, **kwargs):
    self._semaphore = Semaphore(maxconn)
    super().__init__(minconn, maxconn, *args, **kwargs)

  def getconn(self, *args, **kwargs):
    self._semaphore.acquire()
    try:
      return super().getconn(*args, **kwargs)
    except:
      self._semaphore.release()
      raise

  def putconn(self, *args, **kwargs):
    try:
      super().putconn(*args, **kwargs)
    finally:
      self._semaphore.release()

for logname in ['PostgreSQL_event', 'PostgreSQL_error']:
  fd.add_logger.log = fd.add_logger(logname)
  fd.dict_update(PostgreSQL.loggers, '{}'.format(logname), fd.add_logger.log)
