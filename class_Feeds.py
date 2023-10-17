#!/bin/env python3

import psycopg2 as pq
import os
import sys

class IterClass(type):
  def __init__(classobject, classname, baseclasses, attrs):
    pass
  def __iter__(cls):
    return iter(cls._allObjects)

class Feed(object):
  _allObjects = []

  __metaclass__ = IterClass

  def __init__(self, timestamp, message, message_flow = 0):
    self._allObjects.append(self)
    self.timestamp = timestamp
    self.message = message
    self.message_flow = message_flow

  def get_cursor(self, db_conn):
    db_cursor = db_conn.cursor()
    return db_cursor

  def get_list_tables(self, db_cursor):
    db_cursor.execute('show tables')
    curs_tables = db_cursor.fetchall()
    tables_list = []
    for row in curs_tables:
      tables_list.append(row[0])
    return tables_list

  def get_row_count(self, db_cursor, db_name, table_name):
    query = 'select * from {}.{}'.format(db_name, table_name)
    rows = db_cursor.execute(query)
    return rows

  def get_select_limit(self, db_cursor, db_name, table_name):
    query = 'select * from {}.{} limit 1'.format(db_name, table_name)
    one_row = db_cursor.execute(query)
    return one_row

  def get_fields(self):
    return (self.db_brand, self.db_brand_version, self.host, self.domain, self.db_name, self.backup_name, self.backup_location)

  def restore_and_verify(self):
    server = self.host
    print('server: ', server)
    db_conn = self.get_connection(server)
    db_cursor = db_conn.cursor()
    list_databases = self.get_list_databases(db_cursor)
    print(list_databases)
    return('I am restoring: db_brand {}, db_brand_version {}, host {}, database {}'.format(self.db_brand, self.db_brand_version, self.host, self.db_name))

  def toon(self):
    return(self.db_brand, self.db_brand_version, self.host, self.db_name, self.backup_name, self.backup_location)

  def set_create_database(self, db_cursor, db_name):
    db_cursor.execute('create database {}'.format(db_name))

  def set_close_cursor(self, db_cursor):
    db_cursor.close()

  def set_close_connection(self, db_conn):
    db_conn.close()

  def set_query(self, db_cursor, sql):
    db_cursor.execute(sql)

  def set_drop_database(self, db_cursor, db_name):
    db_cursor.execute('drop database {}'.format(db_name))

  def set_restore_database(self, db_cursor, backup_location, backup_name):
    #query=('source {}/{};'.format(backup_location, backup_name))
    query=open('{}/{}, "rt";'.format(backup_location, backup_name))
    return db_cursor.execute(query)

  def set_use_database(self, db_cursor, db_name):
    db_cursor.execute('use {}'.format(db_name))
