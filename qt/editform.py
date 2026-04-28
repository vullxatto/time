from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from libwidget import libWidget

class editForm(QWidget, libWidget):

    def __init__(self, library=None, conf=None, parent=None):
        QWidget.__init__(self, parent)
        libWidget.__init__(self, library=library, conf=conf)
        self.__grid = QGridLayout()
        self.__vbox = QVBoxLayout()
        self.__hbox = QHBoxLayout()
        self.__pbox = QVBoxLayout()
        self.__pixLabel = QLabel()
        self.__pbox.addWidget(self.__pixLabel)
        self.__pbox.addStretch(1)
        self.__vbox.addLayout(self.__grid)
        self.__vbox.addStretch(1)
        self.__hbox.addLayout(self.__pbox)
        self.__hbox.addLayout(self.__vbox)
        self.setLayout(self.__hbox)
        self.__currentCode = None

    def addLabel(self, text, x, y):
        self.__grid.addWidget(QLabel(text), x, y)

    def addNewWidget(self, widget, x, y):
        self.__grid.addWidget(widget, x, y)

    def setPix(self, filename):
        if self.getConf() and filename:
            self.__pixLabel.setPixmap(QPixmap(self.getConf().getImgDir() + filename))

    def setCurrentCode(self, value):
        self.__currentCode = value
        self.update()

    def getCurrentCode(self):
        return self.__currentCode

    def decode(self, qstring):
        return str(qstring.toUtf8()).decode('utf-8')

    def clearContents(self):
        pass

    def setData(self):
        pass

    def update(self):
        self.clearContents()
        self.setData()
