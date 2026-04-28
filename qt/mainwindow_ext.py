from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox, QFileDialog
import sys
import os
from travelcompany_ext import TravelCompany_ext
from datajson_ext import datajson_ext
from dataxml_ext import dataxml_ext
from datasql_ext import datasql_ext
from tabwidget_ext import tabWidget_ext

class mainWindow_ext(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Туристическая фирма — Задание 6')
        self.resize(1650, 900)
        self._last_json_path = None
        self.travel_company = TravelCompany_ext()
        self.tabs = tabWidget_ext(library=self.travel_company, parent=self)
        self.setCentralWidget(self.tabs)
        self.create_menu()
        self.refresh_all_tables()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        new_act = QAction('New', self)
        new_act.triggered.connect(self.new_data)
        file_menu.addAction(new_act)
        file_menu.addSeparator()
        open_json = QAction('Open JSON', self)
        open_json.triggered.connect(self.open_json)
        file_menu.addAction(open_json)
        open_xml = QAction('Open XML', self)
        open_xml.triggered.connect(self.open_xml)
        file_menu.addAction(open_xml)
        open_sql = QAction('Open SQL', self)
        open_sql.triggered.connect(self.open_sql)
        file_menu.addAction(open_sql)
        file_menu.addSeparator()
        save_json = QAction('Save JSON', self)
        save_json.triggered.connect(self.save_json)
        file_menu.addAction(save_json)
        save_xml = QAction('Save XML', self)
        save_xml.triggered.connect(self.save_xml)
        file_menu.addAction(save_xml)
        save_sql = QAction('Save SQL', self)
        save_sql.triggered.connect(self.save_sql)
        file_menu.addAction(save_sql)

    def new_data(self):
        if QMessageBox.question(self, 'New', 'Очистить все данные?') == QMessageBox.Yes:
            self.travel_company.clear()
            self.refresh_all_tables()

    def open_json(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Открыть JSON', '', 'JSON (*.json)')
        if file:
            try:
                self.travel_company.clear()
                djson = datajson_ext(self.travel_company)
                djson.setInp(file)
                djson.read()
                self._last_json_path = os.path.abspath(file)
                self.refresh_all_tables()
                QMessageBox.information(self, 'Успех', 'JSON загружен')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', str(e))

    def open_xml(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Открыть XML', '', 'XML (*.xml)')
        if file:
            try:
                self.travel_company.clear()
                dxml = dataxml_ext(self.travel_company)
                dxml.setInp(file)
                dxml.read()
                self.refresh_all_tables()
                QMessageBox.information(self, 'Успех', 'XML загружен')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', str(e))

    def open_sql(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Открыть SQL', '', 'SQLite (*.sqlite *.db)')
        if file:
            try:
                self.travel_company.clear()
                dsql = datasql_ext(self.travel_company)
                dsql.setInp(file)
                dsql.read()
                self.refresh_all_tables()
                QMessageBox.information(self, 'Успех', 'SQL загружен')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', str(e))

    def save_json(self):
        file, _ = QFileDialog.getSaveFileName(self, 'Сохранить JSON', 'new.json', 'JSON (*.json)')
        if file:
            try:
                djson = datajson_ext(self.travel_company)
                djson.setOut(file)
                djson.write()
                self._last_json_path = os.path.abspath(file)
                QMessageBox.information(self, 'Успех', 'Сохранено в JSON')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', str(e))

    def save_xml(self):
        file, _ = QFileDialog.getSaveFileName(self, 'Сохранить XML', 'new.xml', 'XML (*.xml)')
        if file:
            try:
                dxml = dataxml_ext(self.travel_company)
                dxml.setOut(file)
                dxml.write()
                QMessageBox.information(self, 'Успех', 'Сохранено в XML')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', str(e))

    def save_sql(self):
        file, _ = QFileDialog.getSaveFileName(self, 'Сохранить SQL', 'new.sqlite', 'SQLite (*.sqlite)')
        if file:
            try:
                dsql = datasql_ext(self.travel_company)
                dsql.setOut(file)
                dsql.write()
                QMessageBox.information(self, 'Успех', 'Сохранено в SQL')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', str(e))

    def refresh_all_tables(self):
        if hasattr(self.tabs.clients_tab, 'refreshTable'):
            self.tabs.clients_tab.refreshTable()
        if hasattr(self.tabs.routes_tab, 'refreshTable'):
            self.tabs.routes_tab.refreshTable()
        if hasattr(self.tabs.travels_tab, 'refreshTable'):
            self.tabs.travels_tab.refreshTable()
        if hasattr(self.tabs.airlines_tab, 'refreshTable'):
            self.tabs.airlines_tab.refreshTable()
        if hasattr(self.tabs.operators_tab, 'refreshTable'):
            self.tabs.operators_tab.refreshTable()

    def closeEvent(self, event):
        if self._last_json_path:
            try:
                djson = datajson_ext(self.travel_company)
                djson.setOut(self._last_json_path)
                djson.write()
            except Exception:
                pass
        event.accept()
