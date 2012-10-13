from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QGraphicsPixmapItem
from PyQt4.QtCore import Qt


class QDraggableGraphicsPixmapItem(QGraphicsPixmapItem):
    def __init__(self, filename, pixmap, parent=None, scene=None):
        super(QDraggableGraphicsPixmapItem, self).__init__(pixmap,
                                                          parent,
                                                          scene)
        self._url = "file://" + filename

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            event.ignore()
            return

        self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        drag = QtGui.QDrag(event.widget())
        mime = QtCore.QMimeData()
        drag.setMimeData(mime)
        image = self.pixmap().toImage()
        mime.setImageData(image)
        mime.setUrls([QtCore.QUrl(self._url)])
        drag.setPixmap(self.pixmap())
        drag.exec_(Qt.CopyAction)
        self.setCursor(QtCore.Qt.OpenHandCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(QtCore.Qt.OpenHandCursor)
