import cherrypy

class routepage:

    def __init__(self, library):
        self.__lib = library

    def index(self):
        s = '<a href="../">назад</a> / <a href="addform">добавить маршрут</a><br><br>\n<table border="1" cellpadding="5" cellspacing="0">\n<tr bgcolor="gray">\n<th>№</th><th>Код</th><th>Страна</th><th>Климат</th><th>Длительность</th><th>Отель</th><th>Стоимость</th><th>Действия</th>\n</tr>'
        r = 1
        bg = ''
        for rt in self.__lib.getRouteList():
            code = rt.getCode()
            s += f'<tr{bg}><td>{r}</td><td>{code}</td>'
            s += f"<td>{rt.getName() or ''}</td><td>{rt.getClimate() or ''}</td>"
            s += f"<td>{rt.getDuration()}</td><td>{rt.getHotel() or ''}</td><td>{rt.getCost()}</td>"
            s += f'<td><a href="editform?code={code}">редактировать</a> | '
            s += f'<a href="delr?code={code}">удалить</a></td></tr>'
            r += 1
            bg = '' if bg else ' bgcolor="silver"'
        s += '</table>'
        return s
    index.exposed = True

    def addform(self):
        s = 'Добавить маршрут<br><br>\n<form action="addaction" method="post">\n<table border="0">\n<tr><td>Страна:</td><td><input type="text" name="name" size="40"></td></tr>\n<tr><td>Климат:</td><td><input type="text" name="climate" size="40"></td></tr>\n<tr><td>Длительность (дней):</td><td><input type="number" name="duration" value="7"></td></tr>\n<tr><td>Отель:</td><td><input type="text" name="hotel" size="40"></td></tr>\n<tr><td>Стоимость:</td><td><input type="number" name="cost" value="50000"></td></tr>\n<tr><td colspan="2"><input type="submit" value="Добавить маршрут"></td></tr>\n</table>\n</form><br>\n<a href="index">назад к списку</a>'
        return s
    addform.exposed = True

    def addaction(self, name='', climate='', duration=0, hotel='', cost=0):
        try:
            code = self.__lib.getRouteNewCode()
            self.__lib.createRoute(code, name.strip(), climate.strip(), int(duration), hotel.strip(), int(cost))
            return f"Маршрут добавлен (код {code})<br><a href='index'>назад к списку</a>"
        except Exception as e:
            return f"Ошибка: {e}<br><a href='addform'>назад</a>"
    addaction.exposed = True

    def editform(self, code=0):
        try:
            r = self.__lib.getRoute(int(code))
            s = f'''Редактировать маршрут №{code}<br><br>\n<form action="editaction" method="post">\n<input type="hidden" name="code" value="{code}">\n<table border="0">\n<tr><td>Страна:</td><td><input type="text" name="name" value="{r.getName() or ''}" size="40"></td></tr>\n<tr><td>Климат:</td><td><input type="text" name="climate" value="{r.getClimate() or ''}" size="40"></td></tr>\n<tr><td>Длительность (дней):</td><td><input type="number" name="duration" value="{r.getDuration()}"></td></tr>\n<tr><td>Отель:</td><td><input type="text" name="hotel" value="{r.getHotel() or ''}" size="40"></td></tr>\n<tr><td>Стоимость:</td><td><input type="number" name="cost" value="{r.getCost()}"></td></tr>\n<tr><td colspan="2"><input type="submit" value="Сохранить"></td></tr>\n</table>\n</form><br>\n<a href="index">назад к списку</a>'''
            return s
        except:
            return "Маршрут не найден<br><a href='index'>назад</a>"
    editform.exposed = True

    def editaction(self, code=0, name='', climate='', duration=0, hotel='', cost=0):
        try:
            self.__lib.removeRoute(int(code))
            self.__lib.createRoute(int(code), name.strip(), climate.strip(), int(duration), hotel.strip(), int(cost))
            return f"Маршрут №{code} обновлён<br><a href='index'>назад к списку</a>"
        except Exception as e:
            return f"Ошибка: {e}<br><a href='index'>назад</a>"
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.removeRoute(int(code))
            return f"Маршрут №{code} удалён<br><a href='index'>назад</a>"
        except:
            return "Ошибка удаления<br><a href='index'>назад</a>"
    delr.exposed = True
