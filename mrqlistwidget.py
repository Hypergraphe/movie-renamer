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
from PyQt4.QtGui import QListWidget, QListView, QListWidgetItem
from PyQt4 import QtCore
from moviemodel import GoogleImdbResultCandidate
from observerdp import Observer


class MRQListWidget(QListWidget, Observer):
    def __init__(self, parent = None):
        super(MRQListWidget, self).__init__(parent)
        self.item_to_movie = {}
        self.movie_to_item = {}
                
    def set_model(self, moviemodel):
        self._moviemodel = moviemodel
        self._moviemodel.add_observer(self)


    def closeEditor(self, editor, hint):
        ret = super(QListView, self).closeEditor(editor, hint)
        item = self.currentItem()
        movie = self.item_to_movie[item]
        #if movie.t
        self._moviemodel.affect_candidate(movie,
                GoogleImdbResultCandidate(unicode(item.text()),
                movie.get_imdb_link(),
                movie.get_desc(),
                movie.get_cover()))
        
        return ret

    def update(self, subject):
        action, key = subject

        if action == "add":
            movie = self._moviemodel.data()[-1]
            item = QListWidgetItem(movie.to_string())
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.addItem(item)
            self.item_to_movie[item] = movie
            self.movie_to_item[movie] = item

        if action == "remove":          
            item = self.movie_to_item[key]
            self.takeItem(self.row(item))
            self.item_to_movie.pop(item)
            self.movie_to_item.pop(key)
                        
        if action == "update":
            item = self.movie_to_item[key]
            item.setText(key.to_string())
            self.apply_item_style(key, item)
            if item in self.selectedItems():
                self.emit(QtCore.SIGNAL(\
                "currentItemChanged(QListWidgetItem *,QListWidgetItem *)"),
                          item, item)
            
        if action == "clear":
            item = self.movie_to_item[key]
            item.setText(key.file_basename())
            movie.set_modified(False)
            self.apply_item_style(key, item)   
    
    def apply_item_style(self, movie, item):
        font = item.font()
        font.setBold(movie.has_changed())
        font.setItalic(movie.has_been_saved())
        item.setFont(font)