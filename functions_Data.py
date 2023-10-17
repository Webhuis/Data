#!/usr/bin/env python3

import loglib
import re
import sys

Log = loglib.Logger()

def Exit(ReturnValue):
    Log.log('{0} ended with return code {1}'.format(sys.argv[0].split('/')[-1], ReturnValue))
    #Log.stop(msg=False)
    exit(ReturnValue)

def CheckFail(RC):
    if RC == False:
        raise ValueError

def ToConfig(ConfigNumber):
    cfg = ConfigNumber
    print('cfg ', ConfigNumber)
    print('len cfg', len(cfg))
    if len(cfg) ==  8:
        cfg = cfg[2:]
    if len(cfg) == 6 and re.match('[0-9][0-9][0-9][0-9][0-9][0-9]', cfg):
        pass
    else:
        print('Configuration number ({0}) is not valid'.format(ConfigNumber))
        #print('Configuration number ({0}) is not valid'.format(ConfigNumber), file = sys.stdout)
        #sys.stdout.write('Configuration number ({0}) is not valid'.format(ConfigNumber))
        raise ValueError
    return cfg

def readcfg(cfg_file):
    ValidLine = re.compile('(?!(( | )*(#|$)))').match # APW EXPLAIN!!!
    # (( |  )*(#|$)) == match on start with zero or more spaces or tabs follow
    #              by a # character or an endoffline
    cfg = {}
    with open(cfg_file) as f:
        for line in f.readlines():
            if ValidLine(line) and line.count('=') == 1:
                # Maybe this could be done in the regex..
                item, value = line.strip().split('=')
                cfg[item.strip()] = value.strip().replace('"','')
    return cfg
