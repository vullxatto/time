from PyQt5.QtWidgets import QLineEdit, QSpinBox, QPushButton, QHBoxLayout, QMessageBox, QGridLayout, QLabel, QDialog

class routeEditForm(QDialog):

    def __init__(self, library=None, conf=None, parent=None, code=0):
        super().__init__(parent)
        self.library = library
        self.conf = conf
        self.code = code
        self.setWindowTitle('Редактирование маршрута' if code > 0 else 'Добавление маршрута')
        self.setModal(True)
        self.resize(500, 320)
        self.__nameEdit = QLineEdit()
        self.__climateEdit = QLineEdit()
        self.__durationEdit = QSpinBox()
        self.__hotelEdit = QLineEdit()
        self.__costEdit = QSpinBox()
        self.__durationEdit.setRange(1, 365)
        self.__costEdit.setRange(0, 1000000)
        self.__costEdit.setSingleStep(100)
        layout = QGridLayout(self)
        layout.addWidget(QLabel('Страна:'), 0, 0)
        layout.addWidget(self.__nameEdit, 0, 1)
        layout.addWidget(QLabel('Климат:'), 1, 0)
        layout.addWidget(self.__climateEdit, 1, 1)
        layout.addWidget(QLabel('Длительность (дней):'), 2, 0)
        layout.addWidget(self.__durationEdit, 2, 1)
        layout.addWidget(QLabel('Отель:'), 3, 0)
        layout.addWidget(self.__hotelEdit, 3, 1)
        layout.addWidget(QLabel('Стоимость:'), 4, 0)
        layout.addWidget(self.__costEdit, 4, 1)
        btn_layout = QHBoxLayout()
        self.btnSave = QPushButton('Сохранить')
        self.btnCancel = QPushButton('Отмена')
        btn_layout.addWidget(self.btnSave)
        btn_layout.addWidget(self.btnCancel)
        layout.addLayout(btn_layout, 5, 0, 1, 2)
        self.btnSave.clicked.connect(self.save)
        self.btnCancel.clicked.connect(self.reject)
        self.loadData()

    def loadData(self):
        if self.code > 0:
            try:
                r = self.library.getRoute(self.code)
                self.__nameEdit.setText(r.getName() or '')
                self.__climateEdit.setText(r.getClimate() or '')
                self.__durationEdit.setValue(r.getDuration())
                self.__hotelEdit.setText(r.getHotel() or '')
                self.__costEdit.setValue(r.getCost())
            except:
                pass

    def save(self):
        try:
            if self.code > 0:
                self.library.removeRoute(self.code)
            new_code = self.code if self.code > 0 else self.library.getRouteNewCode()
            self.library.createRoute(new_code, self.__nameEdit.text().strip(), self.__climateEdit.text().strip(), self.__durationEdit.value(), self.__hotelEdit.text().strip(), self.__costEdit.value())
            QMessageBox.information(self, 'Успех', 'Маршрут успешно сохранён!')
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить маршрут:\n{str(e)}')
