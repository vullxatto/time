from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox
from dbtablewidget import dbTableWidget
from clienteditform import clientEditForm

class clientsTable(QWidget):

    def __init__(self, library=None, conf=None, parent=None):
        super().__init__(parent)
        self.library = library
        self.conf = conf
        self.table = dbTableWidget(library=library, conf=conf)
        self.table.setHeader(['Код', 'Фамилия', 'Имя', 'Отчество', 'Адрес', 'Телефон'])
        self.btnAdd = QPushButton('Добавить клиента')
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
        self.btnAdd.clicked.connect(self.addClient)
        self.btnEdit.clicked.connect(self.editClient)
        self.btnDelete.clicked.connect(self.deleteClient)
        self.refreshTable()

    def refreshTable(self):
        self.fillTable()

    def fillTable(self):
        self.table.clearContents()
        lib = self.library
        clients = lib.getClientList()
        self.table.setRowCount(len(clients))
        for r, c in enumerate(clients):
            self.table.setItem(r, 0, QTableWidgetItem(str(c.getCode())))
            self.table.setItem(r, 1, QTableWidgetItem(c.getSurname() or ''))
            self.table.setItem(r, 2, QTableWidgetItem(c.getName() or ''))
            self.table.setItem(r, 3, QTableWidgetItem(c.getSecname() or ''))
            self.table.setItem(r, 4, QTableWidgetItem(c.getAddress() or ''))
            self.table.setItem(r, 5, QTableWidgetItem(c.getPhone() or ''))
            self.table.appendRowCode(r, c.getCode())
        self.table.adjustColumnWidths()

    def addClient(self):
        form = clientEditForm(self.library, self.conf, self, code=0)
        form.finished.connect(self.refreshTable)
        form.exec_()

    def editClient(self):
        code = self.table.getCurrentCode()
        if not code:
            QMessageBox.warning(self, 'Внимание', 'Выберите клиента в таблице!')
            return
        form = clientEditForm(self.library, self.conf, self, code=code)
        form.finished.connect(self.refreshTable)
        form.exec_()

    def deleteClient(self):
        code = self.table.getCurrentCode()
        if not code:
            QMessageBox.warning(self, 'Внимание', 'Выберите клиента!')
            return
        reply = QMessageBox.question(self, 'Удаление', f'Удалить клиента №{code}?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.library.removeClient(code)
            self.refreshTable()
