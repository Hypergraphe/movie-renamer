# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ihm.ui'
#
# Created: Tue Oct  9 15:23:59 2012
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(812, 717)
        MainWindow.setStatusTip(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setMinimumSize(QtCore.QSize(0, 0))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.listView = MRQListWidget(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setMinimumSize(QtCore.QSize(0, 200))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.verticalLayout_7.addWidget(self.listView)
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.label_5 = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_6.addWidget(self.label_5)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.imdbLinkEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.imdbLinkEdit.setEnabled(True)
        self.imdbLinkEdit.setReadOnly(True)
        self.imdbLinkEdit.setObjectName(_fromUtf8("imdbLinkEdit"))
        self.gridLayout.addWidget(self.imdbLinkEdit, 2, 1, 1, 1)
        self.filenamEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.filenamEdit.setEnabled(True)
        self.filenamEdit.setReadOnly(True)
        self.filenamEdit.setObjectName(_fromUtf8("filenamEdit"))
        self.gridLayout.addWidget(self.filenamEdit, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.descriptionEdit = QtGui.QTextBrowser(self.verticalLayoutWidget)
        self.descriptionEdit.setEnabled(True)
        self.descriptionEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.descriptionEdit.setObjectName(_fromUtf8("descriptionEdit"))
        self.horizontalLayout_5.addWidget(self.descriptionEdit)
        self.movieCoverView = QtGui.QGraphicsView(self.verticalLayoutWidget)
        self.movieCoverView.setMinimumSize(QtCore.QSize(160, 230))
        self.movieCoverView.setMaximumSize(QtCore.QSize(160, 230))
        self.movieCoverView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.movieCoverView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.movieCoverView.setObjectName(_fromUtf8("movieCoverView"))
        self.horizontalLayout_5.addWidget(self.movieCoverView)
        self.gridLayout.addLayout(self.horizontalLayout_5, 3, 1, 1, 1)
        self.titleEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.titleEdit.setEnabled(True)
        self.titleEdit.setReadOnly(True)
        self.titleEdit.setObjectName(_fromUtf8("titleEdit"))
        self.gridLayout.addWidget(self.titleEdit, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.line_2 = QtGui.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout_8.addWidget(self.line_2)
        self.label_7 = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_8.addWidget(self.label_7)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.progressBar = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout_9.addWidget(self.progressBar)
        self.cancelJobButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.cancelJobButton.setObjectName(_fromUtf8("cancelJobButton"))
        self.horizontalLayout_9.addWidget(self.cancelJobButton)
        self.verticalLayout_8.addLayout(self.horizontalLayout_9)
        self.verticalLayout_6.addLayout(self.verticalLayout_8)
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 812, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuAide = QtGui.QMenu(self.menubar)
        self.menuAide.setTearOffEnabled(False)
        self.menuAide.setObjectName(_fromUtf8("menuAide"))
        self.menuFichier = QtGui.QMenu(self.menubar)
        self.menuFichier.setObjectName(_fromUtf8("menuFichier"))
        self.menuEdition = QtGui.QMenu(self.menubar)
        self.menuEdition.setObjectName(_fromUtf8("menuEdition"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionAjouter_Des_Fichiers = QtGui.QAction(MainWindow)
        self.actionAjouter_Des_Fichiers.setObjectName(_fromUtf8("actionAjouter_Des_Fichiers"))
        self.actionAjouter_un_dossier = QtGui.QAction(MainWindow)
        self.actionAjouter_un_dossier.setObjectName(_fromUtf8("actionAjouter_un_dossier"))
        self.actionSoumettre_les_hashs = QtGui.QAction(MainWindow)
        self.actionSoumettre_les_hashs.setEnabled(True)
        self.actionSoumettre_les_hashs.setObjectName(_fromUtf8("actionSoumettre_les_hashs"))
        self.actionEnregistrer = QtGui.QAction(MainWindow)
        self.actionEnregistrer.setEnabled(True)
        self.actionEnregistrer.setObjectName(_fromUtf8("actionEnregistrer"))
        self.actionLaunch_rename_assistant = QtGui.QAction(MainWindow)
        self.actionLaunch_rename_assistant.setEnabled(True)
        self.actionLaunch_rename_assistant.setObjectName(_fromUtf8("actionLaunch_rename_assistant"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setMenuRole(QtGui.QAction.QuitRole)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.action_propos = QtGui.QAction(MainWindow)
        self.action_propos.setObjectName(_fromUtf8("action_propos"))
        self.actionCompute_hashes = QtGui.QAction(MainWindow)
        self.actionCompute_hashes.setEnabled(True)
        self.actionCompute_hashes.setObjectName(_fromUtf8("actionCompute_hashes"))
        self.actionLaunch_from_selection = QtGui.QAction(MainWindow)
        self.actionLaunch_from_selection.setObjectName(_fromUtf8("actionLaunch_from_selection"))
        self.actionEttings = QtGui.QAction(MainWindow)
        self.actionEttings.setObjectName(_fromUtf8("actionEttings"))
        self.actionImport_a_file = QtGui.QAction(MainWindow)
        self.actionImport_a_file.setObjectName(_fromUtf8("actionImport_a_file"))
        self.actionImport_a_directory = QtGui.QAction(MainWindow)
        self.actionImport_a_directory.setObjectName(_fromUtf8("actionImport_a_directory"))
        self.menuAide.addAction(self.action_propos)
        self.menuFichier.addAction(self.actionImport_a_file)
        self.menuFichier.addAction(self.actionImport_a_directory)
        self.menuFichier.addSeparator()
        self.menuFichier.addAction(self.actionQuit)
        self.menuEdition.addAction(self.actionEttings)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuEdition.menuAction())
        self.menubar.addAction(self.menuAide.menuAction())
        self.toolBar.addAction(self.actionAjouter_Des_Fichiers)
        self.toolBar.addAction(self.actionAjouter_un_dossier)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionLaunch_rename_assistant)
        self.toolBar.addAction(self.actionLaunch_from_selection)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionEnregistrer)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Movie Collection Renamer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Media Informations", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Title:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Details :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Current Filename:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Current Task Progress", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelJobButton.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAide.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFichier.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdition.setTitle(QtGui.QApplication.translate("MainWindow", "Edition", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Séléctionner des fichiers à ajouter.", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAjouter_Des_Fichiers.setText(QtGui.QApplication.translate("MainWindow", "Add files", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAjouter_Des_Fichiers.setToolTip(QtGui.QApplication.translate("MainWindow", "Ajouter des fichiers", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAjouter_un_dossier.setText(QtGui.QApplication.translate("MainWindow", "Add directory", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSoumettre_les_hashs.setText(QtGui.QApplication.translate("MainWindow", "Submit hashes", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEnregistrer.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLaunch_rename_assistant.setText(QtGui.QApplication.translate("MainWindow", "Batch rename", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_propos.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCompute_hashes.setText(QtGui.QApplication.translate("MainWindow", "Compute hashes", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLaunch_from_selection.setText(QtGui.QApplication.translate("MainWindow", "Batch rename from selection", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEttings.setText(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_a_file.setText(QtGui.QApplication.translate("MainWindow", "Import a file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_a_directory.setText(QtGui.QApplication.translate("MainWindow", "Import a directory", None, QtGui.QApplication.UnicodeUTF8))

from mrqlistwidget import MRQListWidget
