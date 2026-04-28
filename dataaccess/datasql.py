"""Чтение/запись модели в SQLite.

Работает со схемой из пяти таблиц:
    client, routes, package, package_client, package_route

Все запросы параметризованы (?-плейсхолдеры) — корректно обрабатываются
строки со спецсимволами (апострофы, кавычки) и исключаются SQL-инъекции.
"""

import sqlite3 as db
from dataaccess.data import data


class datasql(data):
    """Сериализатор модели в SQLite."""

    def getCurs(self):
        return self.__curs

    def read(self):
        self.__conn = db.connect(self.getInp())
        self.__curs = self.__conn.cursor()
        try:
            self.readTables()
        finally:
            self.__conn.close()

    def write(self):
        self.__conn = db.connect(self.getOut())
        self.__curs = self.__conn.cursor()
        try:
            self.createTables()
            self.writeTables()
            self.__conn.commit()
        finally:
            self.__conn.close()

    # ------------------------------------------------------------------
    # схема
    # ------------------------------------------------------------------
    def createTables(self):
        self.createClientTable()
        self.createRoutesTable()
        self.createPackageTable()
        self.createPackageClientTable()
        self.createPackageRouteTable()

    def createClientTable(self):
        self.getCurs().execute('''
            CREATE TABLE IF NOT EXISTS client (
                code    INTEGER PRIMARY KEY,
                surname TEXT,
                name    TEXT,
                secname TEXT,
                address TEXT,
                phone   TEXT
            );''')

    def createRoutesTable(self):
        self.getCurs().execute('''
            CREATE TABLE IF NOT EXISTS routes (
                code     INTEGER PRIMARY KEY,
                name     TEXT,
                climate  TEXT,
                duration INTEGER,
                hotel    TEXT,
                cost     INTEGER
            );''')

    def createPackageTable(self):
        self.getCurs().execute('''
            CREATE TABLE IF NOT EXISTS package (
                code     INTEGER PRIMARY KEY,
                date     TEXT,
                quantity INTEGER,
                discount INTEGER
            );''')

    def createPackageClientTable(self):
        self.getCurs().execute('''
            CREATE TABLE IF NOT EXISTS package_client (
                code    INTEGER PRIMARY KEY AUTOINCREMENT,
                package INTEGER REFERENCES package(code) ON UPDATE CASCADE ON DELETE CASCADE,
                client  INTEGER REFERENCES client(code)  ON UPDATE CASCADE ON DELETE CASCADE,
                UNIQUE(package, client)
            );''')

    def createPackageRouteTable(self):
        self.getCurs().execute('''
            CREATE TABLE IF NOT EXISTS package_route (
                code    INTEGER PRIMARY KEY AUTOINCREMENT,
                package INTEGER REFERENCES package(code) ON UPDATE CASCADE ON DELETE CASCADE,
                routes  INTEGER REFERENCES routes(code)  ON UPDATE CASCADE ON DELETE CASCADE,
                UNIQUE(package, routes)
            );''')

    # ------------------------------------------------------------------
    # чтение
    # ------------------------------------------------------------------
    def readTables(self):
        self.readClientTable()
        self.readRoutesTable()
        self.readPackageTable()
        self.readPackageClientTable()
        self.readPackageRouteTable()

    def readClientTable(self):
        self.getCurs().execute(
            'SELECT code, surname, name, secname, address, phone FROM client')
        for r in self.getCurs().fetchall():
            self.getLib().createClient(r[0], r[1], r[2], r[3], r[4], r[5])

    def readRoutesTable(self):
        self.getCurs().execute(
            'SELECT code, name, climate, duration, hotel, cost FROM routes')
        for r in self.getCurs().fetchall():
            self.getLib().createRoute(r[0], r[1], r[2], r[3], r[4], r[5])

    def readPackageTable(self):
        self.getCurs().execute(
            'SELECT code, date, quantity, discount FROM package')
        for r in self.getCurs().fetchall():
            self.getLib().createTravel(r[0], r[1], r[2], r[3])

    def readPackageClientTable(self):
        self.getCurs().execute('SELECT package, client FROM package_client')
        for r in self.getCurs().fetchall():
            travel = self.getLib().getTravel(r[0])
            client = self.getLib().getClient(r[1])
            if travel and client:
                travel.appendClient(client)

    def readPackageRouteTable(self):
        self.getCurs().execute('SELECT package, routes FROM package_route')
        for r in self.getCurs().fetchall():
            travel = self.getLib().getTravel(r[0])
            route = self.getLib().getRoute(r[1])
            if travel and route:
                travel.appendRoute(route)

    # ------------------------------------------------------------------
    # запись (параметризовано)
    # ------------------------------------------------------------------
    def writeTables(self):
        self.writeClientTable()
        self.writeRoutesTable()
        self.writePackageTable()
        self.writePackageClientTable()
        self.writePackageRouteTable()

    def writeClientTable(self):
        for c in self.getLib().getClientList():
            self.getCurs().execute(
                'INSERT INTO client(code, surname, name, secname, address, phone) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (c.getCode(), c.getSurname(), c.getName(),
                 c.getSecname(), c.getAddress(), c.getPhone()))

    def writeRoutesTable(self):
        for r in self.getLib().getRouteList():
            self.getCurs().execute(
                'INSERT INTO routes(code, name, climate, duration, hotel, cost) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (r.getCode(), r.getName(), r.getClimate(),
                 r.getDuration(), r.getHotel(), r.getCost()))

    def writePackageTable(self):
        for t in self.getLib().getTravelList():
            self.getCurs().execute(
                'INSERT INTO package(code, date, quantity, discount) '
                'VALUES (?, ?, ?, ?)',
                (t.getCode(), t.getDate(), t.getQuantity(), t.getDiscount()))

    def writePackageClientTable(self):
        for t in self.getLib().getTravelList():
            for cl in t.getClientCodes():
                self.getCurs().execute(
                    'INSERT INTO package_client(package, client) '
                    'VALUES (?, ?)',
                    (t.getCode(), cl))

    def writePackageRouteTable(self):
        for t in self.getLib().getTravelList():
            for rt in t.getRouteCodes():
                self.getCurs().execute(
                    'INSERT INTO package_route(package, routes) '
                    'VALUES (?, ?)',
                    (t.getCode(), rt))
