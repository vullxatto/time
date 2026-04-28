from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox
from dbtablewidget import dbTableWidget
from routeeditform import routeEditForm

class routesTable(QWidget):

    def __init__(self, library=None, conf=None, parent=None):
        super().__init__(parent)
        self.library = library
        self.conf = conf
        self.table = dbTableWidget(library=library, conf=conf)
        self.table.setHeader(['Код', 'Страна', 'Климат', 'Длительность', 'Отель', 'Стоимость'])
        self.btnAdd = QPushButton('Добавить маршрут')
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
        self.btnAdd.clicked.connect(self.addRoute)
        self.btnEdit.clicked.connect(self.editRoute)
        self.btnDelete.clicked.connect(self.deleteRoute)
        self.refreshTable()

    def refreshTable(self):
        self.fillTable()

    def fillTable(self):
        self.table.clearContents()
        lib = self.library
        routes = lib.getRouteList()
        self.table.setRowCount(len(routes))
        for r, rt in enumerate(routes):
            self.table.setItem(r, 0, QTableWidgetItem(str(rt.getCode())))
            self.table.setItem(r, 1, QTableWidgetItem(rt.getName() or ''))
            self.table.setItem(r, 2, QTableWidgetItem(rt.getClimate() or ''))
            self.table.setItem(r, 3, QTableWidgetItem(str(rt.getDuration())))
            self.table.setItem(r, 4, QTableWidgetItem(rt.getHotel() or ''))
            self.table.setItem(r, 5, QTableWidgetItem(str(rt.getCost())))
            self.table.appendRowCode(r, rt.getCode())
        self.table.adjustColumnWidths()

    def addRoute(self):
        form = routeEditForm(self.library, self.conf, self, code=0)
        form.finished.connect(self.refreshTable)
        form.exec_()

    def editRoute(self):
        code = self.table.getCurrentCode()
        if not code:
            QMessageBox.warning(self, 'Внимание', 'Выберите маршрут в таблице!')
            return
        form = routeEditForm(self.library, self.conf, self, code=code)
        form.finished.connect(self.refreshTable)
        form.exec_()

    def deleteRoute(self):
        code = self.table.getCurrentCode()
        if not code:
            QMessageBox.warning(self, 'Внимание', 'Выберите маршрут!')
            return
        reply = QMessageBox.question(self, 'Удаление', f'Удалить маршрут №{code}?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.library.removeRoute(code)
            self.refreshTable()
