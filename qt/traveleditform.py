from PyQt5.QtWidgets import QLineEdit, QSpinBox, QPushButton, QHBoxLayout, QMessageBox, QGridLayout, QLabel, QDialog, QListWidget, QListWidgetItem, QAbstractItemView, QComboBox
from PyQt5.QtCore import Qt

class travelEditForm(QDialog):

    def __init__(self, library=None, conf=None, parent=None, code=0):
        super().__init__(parent)
        self.library = library
        self.conf = conf
        self.code = code
        self.setWindowTitle('Редактирование путёвки' if code > 0 else 'Добавление путёвки')
        self.setModal(True)
        self.resize(720, 620)
        self.__dateEdit = QLineEdit()
        self.__quantityEdit = QSpinBox()
        self.__discountEdit = QSpinBox()
        self.__quantityEdit.setRange(1, 50)
        self.__discountEdit.setRange(0, 100)
        self.__airlineCombo = QComboBox()
        self.__touroperatorCombo = QComboBox()
        self.clientListWidget = QListWidget()
        self.clientListWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.routeListWidget = QListWidget()
        self.routeListWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setup_ui()
        self.load_airline_touroperator_combos()
        self.load_available_items()
        self.loadData()

    def setup_ui(self):
        layout = QGridLayout(self)
        layout.addWidget(QLabel('Дата отправления:'), 0, 0)
        layout.addWidget(self.__dateEdit, 0, 1)
        layout.addWidget(QLabel('Количество человек:'), 1, 0)
        layout.addWidget(self.__quantityEdit, 1, 1)
        layout.addWidget(QLabel('Скидка (%):'), 2, 0)
        layout.addWidget(self.__discountEdit, 2, 1)
        layout.addWidget(QLabel('Авиаперевозчик:'), 3, 0)
        layout.addWidget(self.__airlineCombo, 3, 1)
        layout.addWidget(QLabel('Туроператор:'), 4, 0)
        layout.addWidget(self.__touroperatorCombo, 4, 1)
        layout.addWidget(QLabel('Клиенты (множественный выбор):'), 5, 0, 1, 2)
        layout.addWidget(self.clientListWidget, 6, 0, 1, 2)
        layout.addWidget(QLabel('Маршруты (множественный выбор):'), 7, 0, 1, 2)
        layout.addWidget(self.routeListWidget, 8, 0, 1, 2)
        btn_layout = QHBoxLayout()
        self.btnSave = QPushButton('Сохранить')
        self.btnCancel = QPushButton('Отмена')
        btn_layout.addWidget(self.btnSave)
        btn_layout.addWidget(self.btnCancel)
        layout.addLayout(btn_layout, 9, 0, 1, 2)
        self.btnSave.clicked.connect(self.save)
        self.btnCancel.clicked.connect(self.reject)

    def load_airline_touroperator_combos(self):
        self.__airlineCombo.clear()
        self.__airlineCombo.addItem('— не выбран —', 0)
        for a in self.library.getAirlineList():
            self.__airlineCombo.addItem(f'{a.getName()} (код {a.getCode()})', a.getCode())
        self.__touroperatorCombo.clear()
        self.__touroperatorCombo.addItem('— не выбран —', 0)
        for op in self.library.getTourOperatorList():
            self.__touroperatorCombo.addItem(f'{op.getName()} (код {op.getCode()})', op.getCode())

    def _set_combo_by_code(self, combo, code):
        code = int(code or 0)
        for i in range(combo.count()):
            if combo.itemData(i) == code:
                combo.setCurrentIndex(i)
                return
        combo.setCurrentIndex(0)

    def load_available_items(self):
        self.clientListWidget.clear()
        self.routeListWidget.clear()
        for client in self.library.getClientList():
            text = f'{client.getSurname()} {client.getName()} {client.getSecname()} (код {client.getCode()})'
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, client.getCode())
            self.clientListWidget.addItem(item)
        for route in self.library.getRouteList():
            text = f'{route.getName()} — {route.getHotel()} ({route.getDuration()} дней)'
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, route.getCode())
            self.routeListWidget.addItem(item)

    def loadData(self):
        if self.code > 0:
            try:
                t = self.library.getTravel(self.code)
                self.__dateEdit.setText(t.getDate() or '')
                self.__quantityEdit.setValue(t.getQuantity())
                self.__discountEdit.setValue(t.getDiscount())
                if hasattr(t, 'getAirlineCode'):
                    self._set_combo_by_code(self.__airlineCombo, t.getAirlineCode())
                    self._set_combo_by_code(self.__touroperatorCombo, t.getTourOperatorCode())
                else:
                    self._set_combo_by_code(self.__airlineCombo, 0)
                    self._set_combo_by_code(self.__touroperatorCombo, 0)
                selected_clients = set(t.getClientCodes())
                for i in range(self.clientListWidget.count()):
                    item = self.clientListWidget.item(i)
                    if item.data(Qt.UserRole) in selected_clients:
                        item.setSelected(True)
                selected_routes = set(t.getRouteCodes())
                for i in range(self.routeListWidget.count()):
                    item = self.routeListWidget.item(i)
                    if item.data(Qt.UserRole) in selected_routes:
                        item.setSelected(True)
            except Exception:
                pass

    def save(self):
        try:
            if self.code > 0:
                self.library.removeTravel(self.code)
            new_code = self.code if self.code > 0 else self.library.getTravelNewCode()
            airline_code = int(self.__airlineCombo.currentData() or 0)
            touroperator_code = int(self.__touroperatorCombo.currentData() or 0)
            travel = self.library.createTravel(new_code, self.__dateEdit.text().strip(), self.__quantityEdit.value(), self.__discountEdit.value(), airline_code, touroperator_code)
            for i in range(self.clientListWidget.count()):
                item = self.clientListWidget.item(i)
                if item.isSelected():
                    travel.appendClient(item.data(Qt.UserRole))
            for i in range(self.routeListWidget.count()):
                item = self.routeListWidget.item(i)
                if item.isSelected():
                    travel.appendRoute(item.data(Qt.UserRole))
            QMessageBox.information(self, 'Успех', 'Путёвка успешно сохранена!')
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить путёвку:\n{str(e)}')
