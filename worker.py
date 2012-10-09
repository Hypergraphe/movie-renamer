#    The file is part of the Movie Renamer Collection, a simple
#    python tool to rename and export you Media Library.
#
#    Copyright (C) 2011 Hypergraphe
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# TODO use a Queue to manage producer/consumer see: http://code.activestate.com/recipes/577187-python-thread-pool/

from PyQt4 import QtCore
from threading import Condition
import sys, traceback

class Worker(QtCore.QThread):
    def __init__(self):
        super(Worker, self).__init__()
        self.cond = Condition()
        self.job = None
        self.exit = False
        self.daemon = True
    
    def do(self, job, *args):
        self.cond.acquire()
        self.job = job
        self.args = args
        self.cond.notify()
        self.cond.release()

    def die(self):
        self.cond.acquire()
        self.exit = True
        self.cond.notify()
        self.cond.release()

    def run(self):
        print "Worker initialized"
        while 1:
            self.cond.acquire()
            if self.exit:
                break
            if self.job != None:
                print "Job acquired"
                try:
                    self.job(self.args)                
                except Exception as e:
                    print e
                    traceback.print_exc(file=sys.stdout)                    
                self.job = None
                print "Job teminated"
            self.cond.wait()
            self.cond.release()
        print "Worker dead"
