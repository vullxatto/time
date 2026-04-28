from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QTableWidget
from rowcode import rowCode
from libwidget import libWidget

class dbTableWidget(QTableWidget, libWidget):

    def __init__(self, library=None, conf=None, parent=None, header=[]):
        QTableWidget.__init__(self, parent)
        libWidget.__init__(self, library=library, conf=conf)
        self.__rowCode = rowCode()
        if header:
            self.setHeader(header)
        self.update()

    def setHeader(self, value):
        self.setColumnCount(len(value))
        self.setHorizontalHeaderLabels(value)

    def clearContents(self):
        self.__rowCode.clear()
        QTableWidget.clearContents(self)

    def getCodes(self):
        return self.__rowCode.getCodes()

    def getCurrentCode(self):
        return self.__rowCode.getCode(self.currentRow())

    def setCurrentCode(self, code):
        if code:
            row = self.__rowCode.getRow(code)
            if row is not None:
                self.setCurrentCell(row, 0)

    def appendRowCode(self, row, code):
        self.__rowCode.appendRowCode(row, code)

    def adjustColumnWidths(self):
        self.resizeColumnsToContents()
        hdr = self.horizontalHeader()
        fm = QFontMetrics(hdr.font())
        for col in range(self.columnCount()):
            label = self.model().headerData(col, Qt.Horizontal, Qt.DisplayRole)
            label = '' if label is None else str(label)
            text_w = fm.horizontalAdvance(label) if hasattr(fm, 'horizontalAdvance') else fm.width(label)
            need = text_w + 28
            if self.columnWidth(col) < need:
                self.setColumnWidth(col, need)
        self.resizeRowsToContents()

    def update(self, code=0):
        self.clearContents()
        self.setData()
        self.adjustColumnWidths()
        self.setCurrentCode(code)

    def setData(self):
        pass
