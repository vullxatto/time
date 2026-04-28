import cherrypy
import sys
import os
root_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(root_dir)
sys.path.insert(0, root_dir)
from domain.TravelCompany import TravelCompany
from dataaccess.datajson import datajson
from dataaccess.dataxml import dataxml
from dataaccess.datasql import datasql
from web.clientpage import clientpage
from web.routepage import routepage
from web.travelpage import travelpage

def _format_from_post(dformat):
    if isinstance(dformat, (list, tuple)):
        dformat = dformat[0] if dformat else ''
    return (dformat or '').strip()

def _format_for_open(fname, dformat):
    dformat = _format_from_post(dformat)
    ext = os.path.splitext(fname)[1].lower()
    if ext == '.json':
        return 'JSON'
    if ext == '.xml':
        return 'XML'
    if ext in ('.sqlite', '.db'):
        return 'SQL'
    if dformat in ('JSON', 'XML', 'SQL'):
        return dformat
    return dformat

class start:

    def __init__(self):
        self.__lib = TravelCompany()
        self.__load = False
        self.__fname = ''
        self.__dformat = ''
        self.__dataxml = dataxml(self.__lib)
        self.__datajson = datajson(self.__lib)
        self.__datasql = datasql(self.__lib)
        self.clientpage = clientpage(self.__lib)
        self.routepage = routepage(self.__lib)
        self.travelpage = travelpage(self.__lib)

    def index(self):
        if not self.__load:
            s = '<form action="openfile" method="post">\nОткрыть файл<br>\n<input type="text" name="fname" value="data/dataJSON.json"><br>\n<select name="dformat">\n<option value="JSON" selected>JSON</option>\n<option value="XML">XML</option>\n<option value="SQL">SQL</option>\n</select><br>\n<input type="submit" value="Открыть">\n</form>'
        else:
            sxml = sjson = ssql = ''
            if self.__dformat == 'XML':
                sxml = ' selected'
            elif self.__dformat == 'JSON':
                sjson = ' selected'
            elif self.__dformat == 'SQL':
                ssql = ' selected'
            s = f'<a href="clientpage">Клиенты</a><br>\n<a href="routepage">Маршруты</a><br>\n<a href="travelpage">Путёвки</a><br>\n<hr>\n\n<form action="savefile" method="post">\nСохранить файл<br>\n<input type="text" name="fname" value="{self.__fname}"><br>\n<select name="dformat">\n<option{sjson} value="JSON">JSON</option>\n<option{sxml} value="XML">XML</option>\n<option{ssql} value="SQL">SQL</option>\n</select><br>\n<input type="submit" value="Сохранить">\n</form>\n\n<hr>\n\n<form action="openfile" method="post">\nОткрыть другой файл<br>\n<input type="text" name="fname" value=""><br>\n<select name="dformat">\n<option value="JSON" selected>JSON</option>\n<option value="XML">XML</option>\n<option value="SQL">SQL</option>\n</select><br>\n<input type="submit" value="Открыть">\n</form>'
        return s
    index.exposed = True

    def openfile(self, fname='', dformat=''):
        if not fname:
            return "Ошибка: не указано имя файла!<br><a href='./'>назад</a>"
        try:
            self.__lib.clear()
            fmt = _format_for_open(fname, dformat)
            if fmt == 'XML':
                self.__dataxml.setInp(fname)
                self.__dataxml.read()
            elif fmt == 'JSON':
                self.__datajson.setInp(fname)
                self.__datajson.read()
            elif fmt == 'SQL':
                self.__datasql.setInp(fname)
                self.__datasql.read()
            else:
                return "Неизвестный формат!<br><a href='./'>назад</a>"
            self.__load = True
            self.__fname = fname
            self.__dformat = fmt
            return f"Данные успешно загружены<br><a href='./'>назад</a>"
        except Exception as e:
            return f"Ошибка при открытии {fname}: {e}<br><a href='./'>назад</a>"
    openfile.exposed = True

    def savefile(self, fname='', dformat=''):
        if not fname:
            return "Ошибка: не указано имя файла!<br><a href='./'>назад</a>"
        try:
            fmt = _format_for_open(fname, dformat)
            if fmt == 'XML':
                self.__dataxml.setOut(fname)
                self.__dataxml.write()
            elif fmt == 'JSON':
                self.__datajson.setOut(fname)
                self.__datajson.write()
            elif fmt == 'SQL':
                if os.path.isfile(fname):
                    os.remove(fname)
                self.__datasql.setOut(fname)
                self.__datasql.write()
            return f"Данные успешно сохранены<br><a href='./'>назад</a>"
        except Exception as e:
            return f"Ошибка сохранения: {e}<br><a href='./'>назад</a>"
    savefile.exposed = True
if __name__ == '__main__':
    conf = {'/': {'tools.staticdir.root': os.path.abspath(os.getcwd())}}
    cherrypy.quickstart(start(), '/', conf)
