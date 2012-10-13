# -*- coding: utf-8 -*-
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
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QMainWindow, QFileDialog
from PyQt4.QtGui import QListWidgetItem, QGraphicsScene, QIcon
from guiwindow import Ui_MainWindow
from model.moviemodel import *
import time
from draggablepixmap import QDraggableGraphicsPixmapItem
import icontheme
from config import EXTENSIONS, SLEEP


class Ui_MRMainWindow(Ui_MainWindow):
    def __init__(self, moviemodel, worker):
        self._moviemodel = moviemodel
        self.worker = worker
        self.job_canceled = False

    def setupUi(self, MainWindow):
        super(Ui_MRMainWindow, self).setupUi(MainWindow)
        self._main_window = MainWindow
        self.listView.set_model(self._moviemodel)
        self._graphic_scene = QGraphicsScene()
        self.movieCoverView.setScene(self._graphic_scene)

        self.actionAddFiles.setIcon(icontheme.lookup("add",
                                        icontheme.ICON_SIZE_TOOLBAR))

        QtCore.QObject.connect(self.listView,
                                QtCore.SIGNAL("itemClicked(QListWidgetItem *)"),
                                self.candidates_proposition_menu)

        QtCore.QObject.connect(self.listView,
                               QtCore.SIGNAL("currentItemChanged(\
                               QListWidgetItem *,QListWidgetItem *)"),
                               self.load_movie_infos_in_view)

        QtCore.QObject.connect(self.actionAddFiles,
                               QtCore.SIGNAL("triggered()"),
                               self.add_files)

        QtCore.QObject.connect(self.actionAddDirectory,
                               QtCore.SIGNAL("triggered()"),
                                self.add_directory)

        QtCore.QObject.connect(self.actionLaunchRenameAssistant,
                               QtCore.SIGNAL("triggered()"),
                               self.do_compute)

        QtCore.QObject.connect(self.actionLaunchFromSelection,
                               QtCore.SIGNAL("triggered()"),
                               self.do_compute_from_selection)

        QtCore.QObject.connect(self.actionSave,
                               QtCore.SIGNAL("triggered()"),
                               self.do_batch_save)

        QtCore.QObject.connect(self.cancelJobButton,
                               QtCore.SIGNAL("clicked()"),
                               self.canceljob)

        self.listView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.listView.connect(self.listView,
                        QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                        self.onContext)

        QtCore.QObject.connect(self._main_window,
                                QtCore.SIGNAL("progress(int)"),
                                self.update_progress_bar)

        QtCore.QObject.connect(self._main_window,
                                QtCore.SIGNAL("statusmessage(QString)"),
                                self.update_status_bar)

        QtCore.QObject.connect(self.listView,
                               QtCore.SIGNAL("dropped"),
                               self.file_dropped)

    def file_dropped(self, links):
            self.build_model_from_files(links)

    def load_movie_infos_in_view(self, item, previous):
        if len(self._moviemodel.data()) == 0:
            print 'modele vide'
            self.filenamEdit.setText("")
            self.titleEdit.setText("")
            self.imdbLinkEdit.setText("")
            self.descriptionEdit.setText("")
            self._graphic_scene.clear()
            return

        if item == None:
            return

        movie = self.listView.item_to_movie[item]
        self.filenamEdit.setText(movie.get_filename())
        self.titleEdit.setText(movie.get_title())
        self.imdbLinkEdit.setText(movie.get_imdb_link())
        self.descriptionEdit.setText(movie.get_desc())

        self._graphic_scene.clear()
        if movie.get_cover() != "":
            pixmap = QtGui.QPixmap(movie.get_cover())
            pixmap = pixmap.scaled(self.movieCoverView.size())
            qitem = QDraggableGraphicsPixmapItem(movie.get_cover(), pixmap)
            self._graphic_scene.addItem(qitem)

    def add_files(self):
        file_extensions = " ".join(map((lambda x: "*." + x),
                                       EXTENSIONS))
        files = QFileDialog.getOpenFileNames(
            None,
            "Select one or more files to open",
            "/home",
            "Video Files (" + file_extensions + ")")
        self.build_model_from_files([unicode(x) for x in files])

    def add_directory(self):
        direct = QFileDialog.getExistingDirectory(None,
                        "Open Directory", "/home",
                         QFileDialog.ShowDirsOnly)
        self.build_model_from_files([unicode(direct)])

    def build_model_from_files(self, files=[]):
        files = FileTools.recurse_files(files)
        for movie in xrange(len(files)):
            m = Movie(files[movie])
            self._moviemodel.add_movie(m)

    def onContext(self, point):
        if (len(self._moviemodel.data()) == 0) or (self.worker.job != None):
            return
        menu = QtGui.QMenu("Context Menu", self._main_window)
        assist = QtGui.QAction("Rename assistant", None)
        ignore = QtGui.QAction("Ignore", None)
        remove = QtGui.QAction("Remove", None)
        reset = QtGui.QAction("Undo modifications", None)
        save = QtGui.QAction("Save", None)
        rmall = QtGui.QAction("Remove all", None)

        menu.addAction(assist)
        menu.addAction(reset)
        menu.addAction(save)
        #menu.addAction(ignore)
        menu.addAction(remove)
        menu.addAction(rmall)

        res = menu.exec_(self.listView.mapToGlobal(point))
        item = self.listView.currentItem()
        movie = self.listView.item_to_movie[item]

        if res == save:
            self._moviemodel.save_movie(movie)

        if res == remove:
            self._moviemodel.remove_movie(movie)

        if res == reset:
            self._moviemodel.reset_movie_informations(movie)
            self.load_movie_infos_in_view(item, None)

        if res == assist:
            self.worker.do(self.do_compute_sub, movie)

        if res == ignore:
            pass

        if res == rmall:
            movies = list(self._moviemodel.data())
            for movie in movies:
                self._moviemodel.remove_movie(movie)

    def candidates_proposition_menu(self, item):
        movie = self.listView.item_to_movie[item]
        menu = QtGui.QMenu("Propositions", self._main_window)

        candidates = self._moviemodel.get_candidates(movie)
        if(len(candidates) == 0):
            return
        tmp = {}
        if candidates != []:
            for j in candidates:
                i = unicode(j)
                proposition = i[0:min(len(i), 100)]
                a = QtGui.QAction(proposition, None)
                tmp[a] = j
                menu.addAction(a)
        else:
            pass

        res = menu.exec_(QtGui.QCursor.pos())
        if res != None:
            self._moviemodel.affect_candidate(movie, tmp[res])
            self.load_movie_infos_in_view(item, None)

    def do_compute(self):
        self.worker.do(self.do_compute_sub)

    def do_compute_from_selection(self):
        self.worker.do(self.do_compute_sub, selection=True)

    def update_progress_bar(self, val):
        self.progressBar.setProperty("value", val)

    def update_status_bar(self, val):
        self.statusbar.showMessage(val)

    def do_compute_sub(self, movie=(), selection=False):
        self.job_canceled = False
        self._set_enable_toolbar(False)
        self._main_window.emit(QtCore.SIGNAL("statusmessage(QString)"),
                               "Querying Google. This may take some time ....")
        self._main_window.emit(QtCore.SIGNAL("progress(int)"), 0)
        #allocine_engine = GoogleQuery()
        allocine_engine = AllocineQuery()
        google_engine = GoogleQuery()
        movies = self._moviemodel.data()

        if movie != ():
            movies = [movie[0]]

        if selection:
            indexes = self.listView.selectedIndexes()
            if len(indexes) > 0:
                firstindex = indexes[0]
                movies = movies[firstindex.row():]

        for i in xrange(len(movies)):
            if self.job_canceled:
                self._main_window.emit(QtCore.SIGNAL("statusmessage(QString)"),
                                       "Job cancelled.")
                break
            current_movie = movies[i]
            self._main_window.emit(QtCore.SIGNAL("statusmessage(QString)"),
                                   "Processing: %s"%(current_movie.get_title()))

            query = FileTools.preprocess_query(current_movie.get_title())
            propositions = allocine_engine.extract_results(allocine_engine.query(query))
            if len(propositions) == 0:
                propositions = google_engine.extract_results(google_engine.query(query))
            def sorter(x,y):
                if "title" in x.get_imdb_link():
                    if "title" in y.get_imdb_link():
                        return 0
                    return -1
                return 1
            propositions.sort(sorter)
            self._moviemodel.set_candidates(current_movie, propositions)
            if(len(propositions) > 0):
                self._moviemodel.affect_candidate(current_movie,
                                                  propositions[0])
            self._main_window.emit(QtCore.SIGNAL("progress(int)"),
                                   (i + 1) * 100 / len(movies))
            time.sleep(SLEEP)
        self._main_window.emit(QtCore.SIGNAL("progress(int)"), 0)
        self._main_window.emit(QtCore.SIGNAL("statusmessage(QString)"),
                               "Finished.")
        self._set_enable_toolbar(True)

    def do_batch_save(self):
        self.worker.do(self.do_batch_save_sub)

    def do_batch_save_sub(self, args, kwargs):
        data = self._moviemodel.data()
        for movie in data:
            if movie.has_changed():
                self._moviemodel.save_movie(movie)

    def canceljob(self):
        self.job_canceled = True
        self._main_window.emit(QtCore.SIGNAL("statusmessage(QString)"),
                               "Abording current job. Please wait...")

    def _set_enable_toolbar(self, enabled):
        for action in self.toolBar.actions():
            action.setEnabled(enabled)
