#!/bin/env python3

from multiprocessing import Process
import queue #as queue
from subprocess import Popen, PIPE

class VeresQueue(queue):
    '''
    Placeholder for all information from a command, stdout, stderr, rc values
    '''
    #def __init__(self, command):
    def __init__(self):
        #__init__(self) #, command)
        self.command = command
        self.stdout = ""
        self.stderr = ""
        self.rc = ""

class Worker(Process):
    '''
    Placeholder for all information from a command, stdout, stderr, rc values
    '''
    def __init__(self, queue, live_run = False):
        __init__(self)
        self.queue = queue
        self.live_run = live_run
        self.stdout = ""
        self.stderr = ""
        self.rc = ""

    def run(self):
        while not self.queue.empty():
            # grab work; do something to it (+1); then put the result on the output queue
            work = self.queue.get()
            if  self.live_run == True:
                print("Live Run", end = ' ' )
                self.do_work(work)
            else:
                print("Dry Run", end = ' ' )
                print("{} got {}".format(self.name, work))
            self.queue.task_done()
        else:
            print("queue {} done.".format(self.queue))

    def do_work(self, command):
        '''
        Only one worker will do, because the queues are processed sequentially
        '''
        print('do_work: ', command)
        try:
            process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            print("Popen stdout: ", stdout)
            print("Popen stderr: ", stderr)
        except Exception:
            print("Popen ging fout")
            #Hier moet nog een log actie bij
