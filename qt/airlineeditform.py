from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QGridLayout, QLabel, QDialog, QSpinBox

class airlineEditForm(QDialog):

    def __init__(self, library=None, conf=None, parent=None, code=0):
        super().__init__(parent)
        self.library = library
        self.code = code
        self.setWindowTitle('Редактирование авиаперевозчика' if code > 0 else 'Добавление авиаперевозчика')
        self.setModal(True)
        self.resize(500, 220)
        self.__name = QLineEdit()
        self.__flight_cost = QSpinBox()
        self.__flight_cost.setRange(0, 10000000)
        self.__flight_cost.setSuffix(' ₽')
        layout = QGridLayout(self)
        layout.addWidget(QLabel('Название:'), 0, 0)
        layout.addWidget(self.__name, 0, 1)
        layout.addWidget(QLabel('Стоимость перелёта:'), 1, 0)
        layout.addWidget(self.__flight_cost, 1, 1)
        btn_layout = QHBoxLayout()
        self.btnSave = QPushButton('Сохранить')
        self.btnCancel = QPushButton('Отмена')
        btn_layout.addWidget(self.btnSave)
        btn_layout.addWidget(self.btnCancel)
        layout.addLayout(btn_layout, 2, 0, 1, 2)
        self.btnSave.clicked.connect(self.save)
        self.btnCancel.clicked.connect(self.reject)
        self.loadData()

    def loadData(self):
        if self.code > 0:
            a = self.library.getAirline(self.code)
            self.__name.setText(a.getName())
            self.__flight_cost.setValue(int(a.getFlightCost()))

    def save(self):
        if self.code > 0:
            self.library.removeAirline(self.code)
        new_code = self.code if self.code > 0 else self.library.getAirlineNewCode()
        self.library.createAirline(new_code, self.__name.text().strip(), self.__flight_cost.value())
        QMessageBox.information(self, 'Успех', 'Авиаперевозчик сохранён!')
        self.accept()
