#!/bin/env python3

import psycopg2 as pq
import os
import sys

class IterClass(type):
  def __init__(classobject, classname, baseclasses, attrs):
    pass
  def __iter__(cls):
    return iter(cls._allObjects)

class Database(object):
  _allObjects = []

  __metaclass__ = IterClass

  def __new__(cls, backup_id, db_brand, db_brand_version, host, domain, db_name, backup_name, backup_location):
    subclass_map = {subclass.db_brand: subclass for subclass in cls.__subclasses__()}
    subclass = subclass_map[db_brand]
    instance = super(Database, subclass).__new__(subclass)
    return instance

  def get_connection(self, host="localhost", user="veres", port=3306, password="veres", database="mysql"):
    db_conn = pm.connect(host="localhost", user="veres", port=3306, password="veres", database="mysql")
    return db_conn

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

class MySQL(Database):

  db_brand = 'MySQL'

  _allObjects = []

  __metaclass__ = IterClass

  def __init__(self, backup_id, db_brand, db_brand_version, host, domain, db_name, backup_name, backup_location):
    self._allObjects.append(self)
    self.backup_is = backup_id
    self.db_brand = db_brand
    self.db_brand_version = db_brand_version
    self.host = host
    self.domain = domain
    self.db_name = db_name
    self.backup_name = backup_name
    self.backup_location = backup_location

class PostgreSQL(Database):

  db_brand = 'PostgreSQL'

  _allObjects = []

  __metaclass__ = IterClass

  def __init__(self, db_brand, db_brand_version, host, domain, db_name, backup_name, backup_location):
    self._allObjects.append(self)
    self.db_brand = db_brand
    self.db_brand_version = db_brand_version
    self.host = host
    self.domain = domain
    self.db_name = db_name
    self.backup_name = backup_name
    self.backup_location = backup_location

class Admin(object):

  _allObjects = []

  __metaclass__ = IterClass

  def __init__(self, veres_host, veres_port, veres_db):
    self._allObjects.append(self)
    self.veres_host = veres_host
    self.veres_port = veres_port
    self.veres_db = veres_db
    #return self

  def get_connection(self, user='veres', password='veres'):
    veres_host = self.veres_host
    veres_port = self.veres_port
    veres_db = self.veres_db
    db_conn = pq.connect(host=veres_host, user="veres", port=veres_port, password="veres", database=veres_db)
    return db_conn

  def get_cursor(self, db_conn):
    db_cursor = db_conn.cursor()
    return db_cursor

class Backup(Admin):

  _allObjects = []

  __metaclass__ = IterClass

  def __init__(self, veres_host, veres_port, veres_db, backup_schema):
    self._allObjects.append(self)
    super().__init__(veres_host, veres_port, veres_db)
    self.backup_schema = backup_schema

  def get_work(self, db_cursor, schema_name, backup_table):
    query = 'select * from {}.{}'.format(schema_name, backup_table)
    db_cursor.execute(query)
    work_list = db_cursor.fetchall()
    #work_list = []
    #for row in curs_tables:
    #  tables_list.append(row[0])
    return work_list

    work_list = db_cursor.execute(query)
    return work_list

  def get_old_hdisk_ids(self):
    return self.old_hdisk_ids

  def append_old_hdisk_id(self, hdisk_id):
    self.old_hdisk_ids.append(hdisk_id)

class Host(object):
  _allObjects = []

  __metaclass__ = IterClass

  def __init__(self, hostname, domain, environment ):
    self._allObjects.append(self)
    self.host = hostname
    self.target = domain
    self.luns = environment

  def get_hostname(self):
    return self.hostname

  def get_domain(self):
    return self.domain

  def get_environment(self):
    return self.environment


class OutputFile(object):

  def __init__(self, name, log):
    self.name = name
    self.log = log
    self.file = open(self.name,'w')

  def write(self, msg):
    self.file.write(msg)
    self.log.log(msg)

  def __del__(self):
    self.log.log('{} closed'.format(self.file.name))
    self.file.close()


class ScriptFile(OutputFile):

  def __init__(self, name, header, log):
    OutputFile.__init__(self, name, log)
    self.header = header
    OutputFile.write(self, header)
