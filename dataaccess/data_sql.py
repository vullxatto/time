"""Чтение/запись модели в SQLite.

Работает со схемой из пяти таблиц:
    client, routes, package, package_client, package_route

Все запросы параметризованы (?-плейсхолдеры) — корректно обрабатываются
строки со спецсимволами (апострофы, кавычки) и исключаются SQL-инъекции.
"""

import sqlite3 as db
from dataaccess.data import Data


class DataSql(Data):
    """Сериализатор модели в SQLite."""

    def get_curs(self):
        return self.__curs

    def read(self):
        self.__conn = db.connect(self.get_inp())
        self.__curs = self.__conn.cursor()
        try:
            self.read_tables()
        finally:
            self.__conn.close()

    def write(self):
        self.__conn = db.connect(self.get_out())
        self.__curs = self.__conn.cursor()
        try:
            self.create_tables()
            self.write_tables()
            self.__conn.commit()
        finally:
            self.__conn.close()

    # ------------------------------------------------------------------
    # схема
    # ------------------------------------------------------------------
    def create_tables(self):
        self.create_client_table()
        self.create_routes_table()
        self.create_package_table()
        self.create_package_client_table()
        self.create_package_route_table()

    def create_client_table(self):
        self.get_curs().execute('''
            CREATE TABLE IF NOT EXISTS client (
                code    INTEGER PRIMARY KEY,
                surname TEXT,
                name    TEXT,
                secname TEXT,
                address TEXT,
                phone   TEXT
            );''')

    def create_routes_table(self):
        self.get_curs().execute('''
            CREATE TABLE IF NOT EXISTS routes (
                code     INTEGER PRIMARY KEY,
                name     TEXT,
                climate  TEXT,
                duration INTEGER,
                hotel    TEXT,
                cost     INTEGER
            );''')

    def create_package_table(self):
        self.get_curs().execute('''
            CREATE TABLE IF NOT EXISTS package (
                code     INTEGER PRIMARY KEY,
                date     TEXT,
                quantity INTEGER,
                discount INTEGER
            );''')

    def create_package_client_table(self):
        self.get_curs().execute('''
            CREATE TABLE IF NOT EXISTS package_client (
                code    INTEGER PRIMARY KEY AUTOINCREMENT,
                package INTEGER REFERENCES package(code) ON UPDATE CASCADE ON DELETE CASCADE,
                client  INTEGER REFERENCES client(code)  ON UPDATE CASCADE ON DELETE CASCADE,
                UNIQUE(package, client)
            );''')

    def create_package_route_table(self):
        self.get_curs().execute('''
            CREATE TABLE IF NOT EXISTS package_route (
                code    INTEGER PRIMARY KEY AUTOINCREMENT,
                package INTEGER REFERENCES package(code) ON UPDATE CASCADE ON DELETE CASCADE,
                routes  INTEGER REFERENCES routes(code)  ON UPDATE CASCADE ON DELETE CASCADE,
                UNIQUE(package, routes)
            );''')

    # ------------------------------------------------------------------
    # чтение
    # ------------------------------------------------------------------
    def read_tables(self):
        self.read_client_table()
        self.read_routes_table()
        self.read_package_table()
        self.read_package_client_table()
        self.read_package_route_table()

    def read_client_table(self):
        self.get_curs().execute(
            'SELECT code, surname, name, secname, address, phone FROM client')
        for r in self.get_curs().fetchall():
            self.get_lib().create_client(r[0], r[1], r[2], r[3], r[4], r[5])

    def read_routes_table(self):
        self.get_curs().execute(
            'SELECT code, name, climate, duration, hotel, cost FROM routes')
        for r in self.get_curs().fetchall():
            self.get_lib().create_route(r[0], r[1], r[2], r[3], r[4], r[5])

    def read_package_table(self):
        self.get_curs().execute(
            'SELECT code, date, quantity, discount FROM package')
        for r in self.get_curs().fetchall():
            self.get_lib().create_travel(r[0], r[1], r[2], r[3])

    def read_package_client_table(self):
        self.get_curs().execute('SELECT package, client FROM package_client')
        for r in self.get_curs().fetchall():
            travel = self.get_lib().get_travel(r[0])
            client = self.get_lib().get_client(r[1])
            if travel and client:
                travel.append_client(client)

    def read_package_route_table(self):
        self.get_curs().execute('SELECT package, routes FROM package_route')
        for r in self.get_curs().fetchall():
            travel = self.get_lib().get_travel(r[0])
            route = self.get_lib().get_route(r[1])
            if travel and route:
                travel.append_route(route)

    # ------------------------------------------------------------------
    # запись (параметризовано)
    # ------------------------------------------------------------------
    def write_tables(self):
        self.write_client_table()
        self.write_routes_table()
        self.write_package_table()
        self.write_package_client_table()
        self.write_package_route_table()

    def write_client_table(self):
        for c in self.get_lib().get_client_list():
            self.get_curs().execute(
                'INSERT INTO client(code, surname, name, secname, address, phone) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (c.get_code(), c.get_surname(), c.get_name(),
                 c.get_secname(), c.get_address(), c.get_phone()))

    def write_routes_table(self):
        for r in self.get_lib().get_route_list():
            self.get_curs().execute(
                'INSERT INTO routes(code, name, climate, duration, hotel, cost) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (r.get_code(), r.get_name(), r.get_climate(),
                 r.get_duration(), r.get_hotel(), r.get_cost()))

    def write_package_table(self):
        for t in self.get_lib().get_travel_list():
            self.get_curs().execute(
                'INSERT INTO package(code, date, quantity, discount) '
                'VALUES (?, ?, ?, ?)',
                (t.get_code(), t.get_date(), t.get_quantity(), t.get_discount()))

    def write_package_client_table(self):
        for t in self.get_lib().get_travel_list():
            for cl in t.get_client_codes():
                self.get_curs().execute(
                    'INSERT INTO package_client(package, client) '
                    'VALUES (?, ?)',
                    (t.get_code(), cl))

    def write_package_route_table(self):
        for t in self.get_lib().get_travel_list():
            for rt in t.get_route_codes():
                self.get_curs().execute(
                    'INSERT INTO package_route(package, routes) '
                    'VALUES (?, ?)',
                    (t.get_code(), rt))
