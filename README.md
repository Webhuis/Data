# Data
Data mining, messaging and Data distribution in CFEngine
Help on module class_Data:

NAME
    class_Data - #import psycopg2 as pq

CLASSES
    builtins.object
        Data
    
    class Data(builtins.object)
     |  The Data class architecture has convergence in mind. Convergence is the theoretical model in which agents convergently work towards their desired state.
     |  Data tries to provide the requesters with all the available information that is suitable for the requesting agents.
     |  The agent itself works convergently towards the desired state, which is defined in the role based policies.
     |  This way the information provided by Data enables the agent to make the promises come true.
     |  
     |  Data contains information along the following lines:
     |  - Host data
     |  - Domain data
     |  - Role data
     |  The role may require Data to provide the agent with context information and information about other agents.
     |  
     |  Data receives a message from an agent with agent specific information, which triggers a response containing the above information from Data to the agent.
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  domain_container(self, domain_name)
     |  
     |  domain_role_container(self)
     |  
     |  feed_to_hardclass(self, message, postgres)
     |  
     |  get_fqhost_view(self)
     |      The view consists of the following containers:
     |       - organisation
     |       - domain
     |       - role
     |       - domain role
     |       - services
     |       - config view, every agent
     |       - purpose in life view, for agents that need knowledge about other agents
     |  
     |  organisation_container(self, organisation_name)
     |  
     |  provide_view(self, message)
     |  
     |  role_container(self, role_code)
     |      Contains services
     |  
     |  work_after_response(self, feed_object, fqhost_object)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  _ |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  loggers = {'Data_error': [<loguru.logger handlers=[(id=0, level=10, si...

DATA
    logger = <loguru.logger handlers=[(id=0, level=10, sink=<...el=10, sin...
    logname = 'Data_error'

FILE
    /home/martin/Documents/Organisatie/Webhuis/Projecten/Data_app/Data/class_Data.py_dict__ 

# License
As per the <a href="https://webhuis.nl/index.php?page=gpl-license">LICENSE</a> file, Data is licensed under the Gnu General Public License GPL, version 3.
