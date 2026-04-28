from PyQt5.QtWidgets import QTabWidget
from clientstable import clientsTable
from routestable import routesTable
from travelstable import travelsTable
from airlinestable import airlinesTable
from touroperatorstable import touroperatorsTable

class tabWidget_ext(QTabWidget):

    def __init__(self, library=None, conf=None, parent=None):
        super().__init__(parent)
        self.library = library
        self.conf = conf
        self.clients_tab = clientsTable(library=library, conf=conf, parent=self)
        self.routes_tab = routesTable(library=library, conf=conf, parent=self)
        self.travels_tab = travelsTable(library=library, conf=conf, parent=self)
        self.airlines_tab = airlinesTable(library=library, conf=conf, parent=self)
        self.operators_tab = touroperatorsTable(library=library, conf=conf, parent=self)
        self.addTab(self.clients_tab, 'Клиенты')
        self.addTab(self.routes_tab, 'Маршруты')
        self.addTab(self.travels_tab, 'Путёвки')
        self.addTab(self.airlines_tab, 'Авиаперевозчики')
        self.addTab(self.operators_tab, 'Туроператоры')

    def refresh(self):
        if hasattr(self.clients_tab, 'refreshTable'):
            self.clients_tab.refreshTable()
        if hasattr(self.routes_tab, 'refreshTable'):
            self.routes_tab.refreshTable()
        if hasattr(self.travels_tab, 'refreshTable'):
            self.travels_tab.refreshTable()
        if hasattr(self.airlines_tab, 'refreshTable'):
            self.airlines_tab.refreshTable()
        if hasattr(self.operators_tab, 'refreshTable'):
            self.operators_tab.refreshTable()
