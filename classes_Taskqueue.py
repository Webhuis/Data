#!/usr/bin/env python3

import subprocess as sp
from threading import Thread   # currentThread is not used
import multiprocessing as mp
import queue as q

class TaskQueue(q.Queue):

  def __init__(self, num_workers=1):
    q.Queue.__init__(self)
    self.num_workers = num_workers
    self.start_workers()

  def add_task(self, task):
    self.put(task)

  def start_workers(self):
    for i in range(self.num_workers):
      t = Thread(target=self.worker)
      t.daemon = True
      t.start()

  def worker(self):
    while True:
      tupl = self.get()
      veres_log.info('Thread ended: {} {}'.format(self.worker, tupl))
      tupl()
      self.task_done()
