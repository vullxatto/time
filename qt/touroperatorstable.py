from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox
from dbtablewidget import dbTableWidget
from touroperatoreditform import touroperatorEditForm

class touroperatorsTable(QWidget):

    def __init__(self, library=None, conf=None, parent=None):
        super().__init__(parent)
        self.library = library
        self.conf = conf
        self.table = dbTableWidget(library=library, conf=conf)
        self.table.setHeader(['Код', 'Название', 'Адрес', 'Телефон', 'Сайт'])
        self.btnAdd = QPushButton('Добавить туроператора')
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
        operators = self.library.getTourOperatorList()
        self.table.setRowCount(len(operators))
        for r, t in enumerate(operators):
            self.table.setItem(r, 0, QTableWidgetItem(str(t.getCode())))
            self.table.setItem(r, 1, QTableWidgetItem(t.getName() or ''))
            self.table.setItem(r, 2, QTableWidgetItem(t.getAddress() or ''))
            self.table.setItem(r, 3, QTableWidgetItem(t.getPhone() or ''))
            self.table.setItem(r, 4, QTableWidgetItem(t.getWebsite() or ''))
            self.table.appendRowCode(r, t.getCode())
        self.table.adjustColumnWidths()

    def getCurrentCode(self):
        return self.table.getCurrentCode()

    def add(self):
        form = touroperatorEditForm(self.library, self.conf, self, code=0)
        form.finished.connect(self.refreshTable)
        form.exec_()

    def edit(self):
        code = self.table.getCurrentCode()
        if not code:
            QMessageBox.warning(self, 'Внимание', 'Выберите туроператора в таблице!')
            return
        form = touroperatorEditForm(self.library, self.conf, self, code=code)
        form.finished.connect(self.refreshTable)
        form.exec_()

    def delete(self):
        code = self.table.getCurrentCode()
        if not code:
            QMessageBox.warning(self, 'Внимание', 'Выберите туроператора!')
            return
        reply = QMessageBox.question(self, 'Удаление', f'Удалить туроператора №{code}?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.library.removeTourOperator(code)
            self.refreshTable()
