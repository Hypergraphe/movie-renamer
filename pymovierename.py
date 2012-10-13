#!/usr/bin/python
#-*- Coding: utf-8 -*-

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
from PyQt4.QtGui import QApplication, QMainWindow
from view.ihm import Ui_MRMainWindow
from model.moviemodel import MovieCollectionModel
from tools.worker import Worker
import sys
from tools.ApplicationManager import ApplicationContextManger

if __name__ == "__main__":
    with ApplicationContextManger():
        moviemodel = MovieCollectionModel()
        app = QApplication(sys.argv)
        window = QMainWindow()
        worker = Worker()
        worker.start()
        ui = Ui_MRMainWindow(moviemodel, worker)
        ui.setupUi(window)
        window.show()
        ret = app.exec_()
        ui.job_canceled = True
        worker.die()
    sys.exit(ret)
