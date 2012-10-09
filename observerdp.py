#    The file is part of the Movie Renamer Collection, a simple
#    python tool to rename and export you Media Library.
#
#    Copyright (C) 2011  Hypergraphe
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
"""Observable/Observer Design pattern implementation"""
class Observable(object):
    def __init__(self):
        self._observers = []
        self._has_changed = False

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def set_changed(self):
        self._has_changed = True

    def has_changed(self):
        return self._has_changed

    def notify_all(self, subject=""):
        if self.has_changed():
            for observer in self._observers:
                observer.update(subject)
            self._has_changed = False
    

class Observer(object):
    def __init__(self):
        pass

    def update(self, subject):
        pass
    
