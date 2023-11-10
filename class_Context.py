#!/usr/bin/env python3

from datetime import datetime, timezone

class FQHost(object):

  def __init__(self, uqhost, domain_name, postgres):
    self.uqhost = uqhost
    self.domain_name = domain_name
    self.postgres = postgres
    self.role_code = uqhost[0:4]

  def get_fqhost_services_view(self):
    self.exists = self.check_exists()
    if self.exists == True:
      pass
    else:
      self.query = self.insert_fqhost()
      self.id_fqhost = self.postgres.pool_insert(self.query)

    self.query = ("select row_to_json(x) from (select uqhost, domain_name, service_type, service_port from context.fqhost_services where uqhost = '{}' and domain_name = '{}') as x;"
                 .format(self.uqhost, self.domain_name))
    self.fqhost_role_view = self.postgres.pool_query(self.query)
    return self.fqhost_role_view

  def check_exists(self):
    query = "select exists(select 1 from context.fqhost where uqhost = '{}' and domain_name = '{}');".format(self.uqhost, self.domain_name)
    exists = self.postgres.pool_query(query)
    return exists[0][0]

  def insert_fqhost(self):
    self.timestamp = datetime.now(timezone.utc)
    self.query = ("insert into context.fqhost (uqhost, domain_name, role_code, timestamp)"
                  "values ('{}', '{}', '{}', '{}') returning id;").format(self.uqhost, self.domain_name, self.role_code, self.timestamp)
    return self.query

  def update_fqhost(self):
    self.last_seen = datetime.now(timezone.utc)
    self.query = ("update context.fqhost set last_seen = '{}' where uqhost = '{}' and domain_name = '{}' returning id;").format(self.last_seen, self.uqhost, self.domain_name)
    self.id_fqhost_update = self.postgres.pool_insert(self.query)
    return self.id_fqhost_update

class Organisation(object):

  def __init__(self, organisation, postgres):
    self.organisation = organisation
    self.postgres = postgres

  def get_organisation_data(self, organisation_name):

    self.query =  ("select organisation_name, organisation_data from context.organisation where organisation_name = '{}';").format(organisation_name)
    self.organisation_data = self.postgres.pool_query(self.query)

    return self.organisation_data

class Domain(object):

  def __init__(self, domain, postgres):
    self.domain = domain
    self.postgres = postgres

  def get_domain_data(self, domain_name):

    self.query =  ("select organisation_name, domain_data from context.domain where domain_name = '{}';").format(domain_name)
    print('query', self.postgres.pool_query(self.query))
    organisation_name, domain_data = self.postgres.pool_query(self.query)
    print(organisation_name, domain_data)
    return organisation_name, domain_data

class Role(object):

  def __init__(self, role_code, postgres):
    self.role_code = role_code
    self.postgres = postgres

  def get_role_data(self, role_code):

    self.query =  ("select role_data from context.role where role_code = '{}';").format(role_code)
    self.role_data = self.postgres.pool_query(self.query)

    return self.role_data

class SubDomain(Domain):

  def __init__(self, domain_name, postgres):
    self.domain_name = domain_name
    domain_parts = domain_name.split('.')
    org_domain = '.'.join(domain_parts[1:])
    super().__init__(org_domain, postgres)
    sub_domain = domain_parts[0]
    self.sub_domain = sub_domain

  def get_domain_data(self):

    #self.domain_combined = self.get_domain_info(self.org_domain)
    self.domain_combined += self.get_domain_info(self.domain_name)
    #print('SubDomain',self.domain_combined)

    return self.domain_combined
