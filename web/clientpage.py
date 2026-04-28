import cherrypy

class clientpage:

    def __init__(self, library):
        self.__lib = library

    def index(self):
        s = '<a href="../">назад</a> / <a href="addform">добавить клиента</a><br><br>\n<table border="1" cellpadding="5" cellspacing="0">\n<tr bgcolor="gray">\n<th>№</th><th>Код</th><th>Фамилия</th><th>Имя</th><th>Отчество</th><th>Адрес</th><th>Телефон</th><th>Действия</th>\n</tr>'
        r = 1
        bg = ''
        for c in self.__lib.getClientList():
            code = c.getCode()
            s += f'<tr{bg}><td>{r}</td><td>{code}</td>'
            s += f"<td>{c.getSurname() or ''}</td><td>{c.getName() or ''}</td>"
            s += f"<td>{c.getSecname() or ''}</td><td>{c.getAddress() or ''}</td>"
            s += f"<td>{c.getPhone() or ''}</td>"
            s += f'<td><a href="editform?code={code}">редактировать</a> | '
            s += f'<a href="delr?code={code}">удалить</a></td></tr>'
            r += 1
            bg = '' if bg else ' bgcolor="silver"'
        s += '</table>'
        return s
    index.exposed = True

    def addform(self):
        s = 'Добавить клиента<br><br>\n<form action="addaction" method="post">\n<table border="0">\n<tr><td>Фамилия:</td><td><input type="text" name="surname" size="40"></td></tr>\n<tr><td>Имя:</td><td><input type="text" name="name" size="40"></td></tr>\n<tr><td>Отчество:</td><td><input type="text" name="secname" size="40"></td></tr>\n<tr><td>Адрес:</td><td><input type="text" name="address" size="50"></td></tr>\n<tr><td>Телефон:</td><td><input type="text" name="phone" size="30"></td></tr>\n<tr><td colspan="2"><input type="submit" value="Добавить клиента"></td></tr>\n</table>\n</form><br>\n<a href="index">назад к списку</a>'
        return s
    addform.exposed = True

    def addaction(self, surname='', name='', secname='', address='', phone=''):
        try:
            code = self.__lib.getClientNewCode()
            self.__lib.createClient(code, surname.strip(), name.strip(), secname.strip(), address.strip(), phone.strip())
            return f"Клиент добавлен (код {code})<br><a href='index'>назад к списку</a>"
        except Exception as e:
            return f"Ошибка: {e}<br><a href='addform'>назад</a>"
    addaction.exposed = True

    def editform(self, code=0):
        try:
            c = self.__lib.getClient(int(code))
            s = f'''Редактировать клиента №{code}<br><br>\n<form action="editaction" method="post">\n<input type="hidden" name="code" value="{code}">\n<table border="0">\n<tr><td>Фамилия:</td><td><input type="text" name="surname" value="{c.getSurname() or ''}" size="40"></td></tr>\n<tr><td>Имя:</td><td><input type="text" name="name" value="{c.getName() or ''}" size="40"></td></tr>\n<tr><td>Отчество:</td><td><input type="text" name="secname" value="{c.getSecname() or ''}" size="40"></td></tr>\n<tr><td>Адрес:</td><td><input type="text" name="address" value="{c.getAddress() or ''}" size="50"></td></tr>\n<tr><td>Телефон:</td><td><input type="text" name="phone" value="{c.getPhone() or ''}" size="30"></td></tr>\n<tr><td colspan="2"><input type="submit" value="Сохранить"></td></tr>\n</table>\n</form><br>\n<a href="index">назад к списку</a>'''
            return s
        except:
            return "Клиент не найден<br><a href='index'>назад</a>"
    editform.exposed = True

    def editaction(self, code=0, surname='', name='', secname='', address='', phone=''):
        try:
            self.__lib.removeClient(int(code))
            self.__lib.createClient(int(code), surname.strip(), name.strip(), secname.strip(), address.strip(), phone.strip())
            return f"Клиент №{code} обновлён<br><a href='index'>назад к списку</a>"
        except Exception as e:
            return f"Ошибка: {e}<br><a href='index'>назад</a>"
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.removeClient(int(code))
            return f"Клиент №{code} удалён<br><a href='index'>назад</a>"
        except:
            return "Ошибка удаления<br><a href='index'>назад</a>"
    delr.exposed = True
