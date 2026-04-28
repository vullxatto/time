from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox
from dbtablewidget import dbTableWidget
from traveleditform import travelEditForm

class travelsTable(QWidget):

    def __init__(self, library=None, conf=None, parent=None):
        super().__init__(parent)
        self.library = library
        self.conf = conf
        self.table = dbTableWidget(library=library, conf=conf)
        self.table.setHeader(['Код', 'Дата', 'Кол-во', 'Скидка %', 'Авиаперевозчик', 'Туроператор', 'Клиенты', 'Маршруты'])
        self.btnAdd = QPushButton('Добавить путёвку')
        self.btnEdit = QPushButton('Изменить')
        self.btnDelete = QPushButton('Удалить')
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btnAdd)
        btn_layout.addWidget(self.btnEdit)
        btn_layout.addWidget(self.btnDelete)
        btn_layout.addStretch()
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table)
        self.btnAdd.clicked.connect(self.addTravel)
        self.btnEdit.clicked.connect(self.editTravel)
        self.btnDelete.clicked.connect(self.deleteTravel)
        self.refreshTable()

    def refreshTable(self):
        self.fillTable()

    def _airline_label(self, t):
        if not hasattr(t, 'getAirlineCode'):
            return '—'
        c = t.getAirlineCode()
        if not c:
            return '—'
        a = self.library.getAirline(c)
        return a.getName() if a else str(c)

    def _touroperator_label(self, t):
        if not hasattr(t, 'getTourOperatorCode'):
            return '—'
        c = t.getTourOperatorCode()
        if not c:
            return '—'
        op = self.library.getTourOperator(c)
        return op.getName() if op else str(c)

    def fillTable(self):
        self.table.clearContents()
        travels = self.library.getTravelList()
        self.table.setRowCount(len(travels))
        for r, t in enumerate(travels):
            clients_str = ', '.join((str(c) for c in t.getClientCodes())) if t.getClientCodes() else '—'
            routes_str = ', '.join((str(c) for c in t.getRouteCodes())) if t.getRouteCodes() else '—'
            self.table.setItem(r, 0, QTableWidgetItem(str(t.getCode())))
            self.table.setItem(r, 1, QTableWidgetItem(t.getDate() or ''))
            self.table.setItem(r, 2, QTableWidgetItem(str(t.getQuantity())))
            self.table.setItem(r, 3, QTableWidgetItem(str(t.getDiscount())))
            self.table.setItem(r, 4, QTableWidgetItem(self._airline_label(t)))
            self.table.setItem(r, 5, QTableWidgetItem(self._touroperator_label(t)))
            self.table.setItem(r, 6, QTableWidgetItem(clients_str))
            self.table.setItem(r, 7, QTableWidgetItem(routes_str))
            self.table.appendRowCode(r, t.getCode())
        self.table.adjustColumnWidths()

    def addTravel(self):
        form = travelEditForm(self.library, self.conf, self, code=0)
        form.finished.connect(self.refreshTable)
        form.exec_()

    def editTravel(self):
        code = self.table.getCurrentCode()
        if not code:
            QMessageBox.warning(self, 'Внимание', 'Выберите путёвку в таблице!')
            return
        form = travelEditForm(self.library, self.conf, self, code=code)
        form.finished.connect(self.refreshTable)
        form.exec_()

    def deleteTravel(self):
        code = self.table.getCurrentCode()
        if not code:
            QMessageBox.warning(self, 'Внимание', 'Выберите путёвку!')
            return
        reply = QMessageBox.question(self, 'Удаление', f'Удалить путёвку №{code}?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.library.removeTravel(code)
            self.refreshTable()
