from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QGridLayout, QLabel, QDialog

class clientEditForm(QDialog):

    def __init__(self, library=None, conf=None, parent=None, code=0):
        super().__init__(parent)
        self.library = library
        self.conf = conf
        self.code = code
        self.setWindowTitle('Редактирование клиента' if code > 0 else 'Добавление клиента')
        self.setModal(True)
        self.resize(480, 300)
        self.__surname = QLineEdit()
        self.__name = QLineEdit()
        self.__secname = QLineEdit()
        self.__address = QLineEdit()
        self.__phone = QLineEdit()
        layout = QGridLayout(self)
        layout.addWidget(QLabel('Фамилия:'), 0, 0)
        layout.addWidget(self.__surname, 0, 1)
        layout.addWidget(QLabel('Имя:'), 1, 0)
        layout.addWidget(self.__name, 1, 1)
        layout.addWidget(QLabel('Отчество:'), 2, 0)
        layout.addWidget(self.__secname, 2, 1)
        layout.addWidget(QLabel('Адрес:'), 3, 0)
        layout.addWidget(self.__address, 3, 1)
        layout.addWidget(QLabel('Телефон:'), 4, 0)
        layout.addWidget(self.__phone, 4, 1)
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
                c = self.library.getClient(self.code)
                self.__surname.setText(c.getSurname() or '')
                self.__name.setText(c.getName() or '')
                self.__secname.setText(c.getSecname() or '')
                self.__address.setText(c.getAddress() or '')
                self.__phone.setText(c.getPhone() or '')
            except Exception as e:
                print('Ошибка загрузки данных клиента:', e)

    def save(self):
        try:
            if self.code > 0:
                self.library.removeClient(self.code)
            new_code = self.code if self.code > 0 else self.library.getClientNewCode()
            self.library.createClient(new_code, self.__surname.text().strip(), self.__name.text().strip(), self.__secname.text().strip(), self.__address.text().strip(), self.__phone.text().strip())
            QMessageBox.information(self, 'Успех', 'Клиент успешно сохранён!')
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить клиента:\n{str(e)}')
