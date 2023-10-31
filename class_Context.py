#!/usr/bin/env python3

class FQHost(object):

  def __init__(self, uqhost, domain):
    self.uqhost = uqhost
    self.domain = domain
    role_code = uqhost[0:4]
    self.role_code = role_code
    return self

class Role(object):

  def __init__(self, role_code):
    self.role_code = role_code

class Domain(object):

  def __init__(self, domain):
    self.domain = domain

