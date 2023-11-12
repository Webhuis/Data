#!/usr/bin/env python3

from datetime import datetime, timezone
import json
import functions_Data as fd

class FQHost(object):

  def __init__(self, uqhost, domain_name, postgres):
    self.uqhost = uqhost
    self.domain_name = domain_name
    self.postgres = postgres
    self.role_code = uqhost[0:4]

  def get_fqhost_view(self):
    self.exists = self.check_exists()
    if self.exists == True:
      pass
    else:
      self.query = self.insert_fqhost()
      self.id_fqhost = self.postgres.pool_insert(self.query)

    #self.query = ("select row_to_json(x) from (select uqhost, domain_name, fqhost_data from context.fqhost where uqhost = '{}' and domain_name = '{}') as x;"
    self.query = "select fqhost_data from context.fqhost where uqhost = '{}' and domain_name = '{}';"
                 .format(self.uqhost, self.domain_name))
    self.fqhost_data = self.postgres.pool_query(self.query)
    print('fqhost_data', self.fqhost_data)

    self.query =  "select organisation_name, domain_data from context.domain where domain_name = '{}';".format(domain_name)
    domain_data_list = self.postgres.pool_query(self.query)
    domain_data = domain_data_list[0]
    organisation_name = domain_data[0]
    domain_data = domain_data[1]
    print('domain_view', self.domain_view)

    self.query =  "select organisation_name, organisation_data from context.organisation where organisation_name = '{}';".format(organisation_name)
    self.organisation_data_list = self.postgres.pool_query(self.query)
    self.organisation_name = self.organisation_data[0][0]
    self.organisation_data = self.organisation_data[0][1]
    organisation_view = fd.to_json(organisation_name, [ self.organisation_data ])
    print('organisation_view', organisation_view)

    self.query = "select domain_role_data from context.domain_role where domain_name = '{}' and role_code = '{}';"
                 .format(self.domain_name, self.role_code))
    self.domain_role_data = self.postgres.pool_query(self.query)
    domain_role_view = fd.to_json(domain_role_name, [ self.domain_role_data ])
    print('domain_role_view', self.domain_role_view)

    self.query =  """select row_to_json(x) from (select ndr.vlan_name, ndr.network_name, n.network_address, n.gateway_address
                     from context.network_domain_role as ndr
                     join context.network as n
                       on ndr.network_name = n.network_name
                     where ndr.domain_name = '{}'
                       and ndr.role_code = '{}' as x;""".format(self.domain_name, self.role_code)

    domain_role_network_view = self.postgres.pool_query(self.query)
    print('domain_role_network_view', self.domain_role_network_view)

    domain_role_network = fd.to_json('domain_role_network', [ domain_role_view, domain_role_network_view ])


    fqhost_view = fd.to_json('fqhost_view', [ self.fqhost_data, self.organisation_data, self.domain_data, self.role_info])

    return fqhost_view

  def check_exists(self):
    query = "select exists(select 1 from context.fqhost where uqhost = '{}' and domain_name = '{}');".format(self.uqhost, self.domain_name)
    exists = self.postgres.pool_query(query)
    return exists[0][0]

  def insert_fqhost(self):
    self.timestamp = datetime.now(timezone.utc)
    self.query = ("insert into context.fqhost (uqhost, domain_name, role_code, timestamp, )"
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

    self.query =  ("select organisation_data from context.organisation where organisation_name = '{}';").format(organisation_name)
    self.organisation_data = self.postgres.pool_query(self.query)
    self.organisation_data = self.organisation_data[0][0]
    return self.organisation_data

class Domain(object):

  def __init__(self, domain, postgres):
    self.domain = domain
    self.postgres = postgres

  def get_domain_data(self, domain_name):

    self.query =  ("select organisation_name, domain_data from context.domain where domain_name = '{}';").format(domain_name)
    domain_data_list = self.postgres.pool_query(self.query)
    domain_data = domain_data_list[0]
    organisation_name = domain_data[0]
    domain_data = domain_data[1]
    return organisation_name, domain_data

class Role(object):

  def __init__(self, role_code, postgres):
    self.role_code = role_code
    self.postgres = postgres

  def get_role_data(self, role_code):

    self.query =  ("select role_data from context.role where role_code = '{}';").format(role_code)
    self.role_data = self.postgres.pool_query(self.query)
    self.role_data = self.role_data[0][0]
    self.query =  """select s.service_port, s.service_name, s.check_line, s.interface
                     from context.service as s
                     join context.role_service as rs
                       on s.service_type = rs.service_type
                     where rs.role_code = '{}';""".format(role_code)
    services  = self.postgres.pool_query(self.query)

    services_to_json = fd.to_json('services', services)
    role_to_json = fd.to_json(self.role_code, [ self.role_data, services_to_json ])
    self.role_info = json.dumps(role_to_json)
    return self.role_info
