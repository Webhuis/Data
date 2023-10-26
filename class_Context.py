#!/usr/bin/env python3

class Domain(object):

  _allObjects = []

  __metaclass__ = IterClass

  def __init__(self, domain_name):
    self.domain_name = domain_name

class Role(object):

  _allObjects = []

  __metaclass__ = IterClass

  def __init__(self, role_code):
    self.role_code = role_code

class Host(object):

  _allObjects = []

  __metaclass__ = IterClass

  def __init__(self, uqhost, domain):
    self.uqhost = uqhost
    self.domain = domain
    role_code = uqhost[0:4]
    self.role_code = role_code

