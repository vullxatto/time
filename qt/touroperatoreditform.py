from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QGridLayout, QLabel, QDialog

class touroperatorEditForm(QDialog):

    def __init__(self, library=None, conf=None, parent=None, code=0):
        super().__init__(parent)
        self.library = library
        self.code = code
        self.setWindowTitle('Редактирование туроператора' if code > 0 else 'Добавление туроператора')
        self.setModal(True)
        self.resize(550, 300)
        self.__name = QLineEdit()
        self.__address = QLineEdit()
        self.__phone = QLineEdit()
        self.__website = QLineEdit()
        layout = QGridLayout(self)
        layout.addWidget(QLabel('Название:'), 0, 0)
        layout.addWidget(self.__name, 0, 1)
        layout.addWidget(QLabel('Адрес:'), 1, 0)
        layout.addWidget(self.__address, 1, 1)
        layout.addWidget(QLabel('Телефон:'), 2, 0)
        layout.addWidget(self.__phone, 2, 1)
        layout.addWidget(QLabel('Сайт:'), 3, 0)
        layout.addWidget(self.__website, 3, 1)
        btn_layout = QHBoxLayout()
        self.btnSave = QPushButton('Сохранить')
        self.btnCancel = QPushButton('Отмена')
        btn_layout.addWidget(self.btnSave)
        btn_layout.addWidget(self.btnCancel)
        layout.addLayout(btn_layout, 4, 0, 1, 2)
        self.btnSave.clicked.connect(self.save)
        self.btnCancel.clicked.connect(self.reject)
        self.loadData()

    def loadData(self):
        if self.code > 0:
            t = self.library.getTourOperator(self.code)
            self.__name.setText(t.getName())
            self.__address.setText(t.getAddress())
            self.__phone.setText(t.getPhone())
            self.__website.setText(t.getWebsite())

    def save(self):
        if self.code > 0:
            self.library.removeTourOperator(self.code)
        new_code = self.code if self.code > 0 else self.library.getTourOperatorNewCode()
        self.library.createTourOperator(new_code, self.__name.text().strip(), self.__address.text().strip(), self.__phone.text().strip(), self.__website.text().strip())
        QMessageBox.information(self, 'Успех', 'Туроператор сохранён!')
        self.accept()
