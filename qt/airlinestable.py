from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox
from dbtablewidget import dbTableWidget
from airlineeditform import airlineEditForm

class airlinesTable(QWidget):

    def __init__(self, library=None, conf=None, parent=None):
        super().__init__(parent)
        self.library = library
        self.conf = conf
        self.table = dbTableWidget(library=library, conf=conf)
        self.table.setHeader(['Код', 'Название', 'Стоимость перелёта'])
        self.btnAdd = QPushButton('Добавить авиаперевозчика')
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
        self.btnAdd.clicked.connect(self.add)
        self.btnEdit.clicked.connect(self.edit)
        self.btnDelete.clicked.connect(self.delete)
        self.refreshTable()

    def refreshTable(self):
        self.fillTable()

    def fillTable(self):
        self.table.clearContents()
        airlines = self.library.getAirlineList()
        self.table.setRowCount(len(airlines))
        for r, a in enumerate(airlines):
            self.table.setItem(r, 0, QTableWidgetItem(str(a.getCode())))
            self.table.setItem(r, 1, QTableWidgetItem(a.getName() or ''))
            self.table.setItem(r, 2, QTableWidgetItem(str(a.getFlightCost())))
            self.table.appendRowCode(r, a.getCode())
        self.table.adjustColumnWidths()

    def getCurrentCode(self):
        return self.table.getCurrentCode()

    def add(self):
        form = airlineEditForm(self.library, self.conf, self, code=0)
        form.finished.connect(self.refreshTable)
        form.exec_()

    def edit(self):
        code = self.table.getCurrentCode()
        if not code:
            QMessageBox.warning(self, 'Внимание', 'Выберите авиаперевозчика в таблице!')
            return
        form = airlineEditForm(self.library, self.conf, self, code=code)
        form.finished.connect(self.refreshTable)
        form.exec_()

    def delete(self):
        code = self.table.getCurrentCode()
        if not code:
            QMessageBox.warning(self, 'Внимание', 'Выберите авиаперевозчика!')
            return
        reply = QMessageBox.question(self, 'Удаление', f'Удалить авиаперевозчика №{code}?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.library.removeAirline(code)
            self.refreshTable()
