from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from airlinestable import airlinesTable
from airlineeditform import airlineEditForm

class airlinePage(QWidget):

    def __init__(self, library=None, conf=None, parent=None):
        super().__init__(parent)
        self.library = library
        self.table = airlinesTable(library=library, conf=conf, parent=self)
        btn_layout = QHBoxLayout()
        self.btnAdd = QPushButton('Добавить авиаперевозчика')
        self.btnEdit = QPushButton('Изменить')
        self.btnDelete = QPushButton('Удалить')
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
        self.refresh()

    def refresh(self):
        self.table.setData()

    def add(self):
        form = airlineEditForm(self.library, None, self, code=0)
        form.finished.connect(self.refresh)
        form.exec_()

    def edit(self):
        code = self.table.getCurrentCode()
        if not code:
            QMessageBox.warning(self, 'Внимание', 'Выберите авиаперевозчика в таблице!')
            return
        form = airlineEditForm(self.library, None, self, code=code)
        form.finished.connect(self.refresh)
        form.exec_()

    def delete(self):
        code = self.table.getCurrentCode()
        if not code:
            QMessageBox.warning(self, 'Внимание', 'Выберите авиаперевозчика!')
            return
        reply = QMessageBox.question(self, 'Удаление', f'Удалить авиаперевозчика №{code}?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.library.removeAirline(code)
            self.refresh()
