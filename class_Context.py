#!/usr/bin/env python3

from datetime import datetime, timezone

class FQHost(object):

  def __init__(self, uqhost, domain_name, postgres):
    self.uqhost = uqhost
    self.domain_name = domain_name
    self.postgres = postgres
    role_code = uqhost[0:4]
    self.role_code = role_code

  def get_fqhost_view(self):
    self.exists = self.check_exists()
    if self.exists == True:
      pass
    else:
      self.query = self.insert_fqhost()
      self.id_fqhost = self.postgres.pool_insert(self.query)
      self.postgres.commit()

    self.query = ('select uqhost, domain_name, role_code, service_type, service_port from context.fqhost_role where uqhost = {} and domain_name = {};'
             .format(self.uqhost, self.domain_name))
    self.fqhost_role_view = self.postgres.pool_query(query)
    return self.fqhost_role_view

  def check_exists(self):
    query = "select exists(select 1 from context.fqhost where uqhost = '{}' and domain_name = '{}');".format(self.uqhost, self.domain_name)
    exists = self.postgres.pool_query(query)
    return exists[0][0]

  def insert_fqhost(self):
    self.timestamp = datetime.now(timezone.utc)
    self.query = ("insert into context.fqhost (uqhost, domain_name, role_code, timestamp)"
                  "values ('{}', '{}', '{}', '{}') returning id;)".format(self.uqhost, self.domain_name, self.role_code, self.timestamp))
    return self.query

class Role(object):

  def __init__(self, role_code):
    self.role_code = role_code

class Domain(object):

  def __init__(self, domain_name):
    self.domain_name = domain_name

