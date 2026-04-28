"""SQLite-сериализация расширенной модели.

Дополняет схему `datasql` четырьмя новыми таблицами (airline, touroperator,
manager, payment) и тремя FK-колонками в таблице package
(airline_code, touroperator_code, manager_code).
"""

import sqlite3
from dataaccess.datasql import datasql


class datasql_ext(datasql):
    """Сериализатор расширенной модели в SQLite."""

    # ------------------------------------------------------------------
    # схема
    # ------------------------------------------------------------------
    def createTables(self):
        super().createTables()
        # дополняем package колонками-FK; ALTER падает, если столбец уже есть —
        # это нормально при повторной записи в существующий файл.
        for col in ('airline_code', 'touroperator_code', 'manager_code'):
            try:
                self.getCurs().execute(
                    f'ALTER TABLE package ADD COLUMN {col} INTEGER DEFAULT 0')
            except sqlite3.OperationalError:
                pass
        self.createAirlineTable()
        self.createTourOperatorTable()
        self.createManagerTable()
        self.createPaymentTable()

    def createAirlineTable(self):
        self.getCurs().execute('''
            CREATE TABLE IF NOT EXISTS airline (
                code        INTEGER PRIMARY KEY,
                name        TEXT,
                flight_cost INTEGER
            );''')

    def createTourOperatorTable(self):
        self.getCurs().execute('''
            CREATE TABLE IF NOT EXISTS touroperator (
                code    INTEGER PRIMARY KEY,
                name    TEXT,
                address TEXT,
                phone   TEXT,
                website TEXT
            );''')

    def createManagerTable(self):
        self.getCurs().execute('''
            CREATE TABLE IF NOT EXISTS manager (
                code     INTEGER PRIMARY KEY,
                surname  TEXT,
                name     TEXT,
                secname  TEXT,
                position TEXT,
                phone    TEXT,
                email    TEXT
            );''')

    def createPaymentTable(self):
        # связь 1:1 с путёвкой обеспечивается UNIQUE на package_code
        self.getCurs().execute('''
            CREATE TABLE IF NOT EXISTS payment (
                code         INTEGER PRIMARY KEY,
                package_code INTEGER UNIQUE
                             REFERENCES package(code)
                             ON UPDATE CASCADE ON DELETE CASCADE,
                date         TEXT,
                amount       INTEGER,
                method       TEXT,
                status       TEXT
            );''')

    # ------------------------------------------------------------------
    # чтение
    # ------------------------------------------------------------------
    def readTables(self):
        super().readTables()
        self.readAirlineTable()
        self.readTourOperatorTable()
        self.readManagerTable()
        self.readPaymentTable()

    def readPackageTable(self):
        try:
            self.getCurs().execute(
                'SELECT code, date, quantity, discount, '
                '       COALESCE(airline_code, 0), '
                '       COALESCE(touroperator_code, 0), '
                '       COALESCE(manager_code, 0) '
                'FROM package')
            for r in self.getCurs().fetchall():
                self.getLib().createTravel(
                    r[0], r[1], r[2], r[3], int(r[4]), int(r[5]), int(r[6]))
        except sqlite3.OperationalError:
            # старая БД без расширенных колонок — fallback на базовую схему
            self.getCurs().execute(
                'SELECT code, date, quantity, discount FROM package')
            for r in self.getCurs().fetchall():
                self.getLib().createTravel(r[0], r[1], r[2], r[3])

    def readAirlineTable(self):
        try:
            self.getCurs().execute('SELECT code, name, flight_cost FROM airline')
            for r in self.getCurs().fetchall():
                self.getLib().createAirline(r[0], r[1], r[2])
        except sqlite3.OperationalError:
            pass

    def readTourOperatorTable(self):
        try:
            self.getCurs().execute(
                'SELECT code, name, address, phone, website FROM touroperator')
            for r in self.getCurs().fetchall():
                self.getLib().createTourOperator(r[0], r[1], r[2], r[3], r[4])
        except sqlite3.OperationalError:
            pass

    def readManagerTable(self):
        try:
            self.getCurs().execute(
                'SELECT code, surname, name, secname, position, phone, email '
                'FROM manager')
            for r in self.getCurs().fetchall():
                self.getLib().createManager(
                    r[0], r[1], r[2], r[3], r[4], r[5], r[6])
        except sqlite3.OperationalError:
            pass

    def readPaymentTable(self):
        try:
            self.getCurs().execute(
                'SELECT code, package_code, date, amount, method, status '
                'FROM payment')
            for r in self.getCurs().fetchall():
                self.getLib().createPayment(
                    r[0], r[1], r[2], r[3], r[4], r[5])
        except sqlite3.OperationalError:
            pass

    # ------------------------------------------------------------------
    # запись
    # ------------------------------------------------------------------
    def writeTables(self):
        super().writeTables()
        self.writeAirlineTable()
        self.writeTourOperatorTable()
        self.writeManagerTable()
        self.writePaymentTable()

    def writePackageTable(self):
        # переопределяем, чтобы записать дополнительные FK-колонки
        for t in self.getLib().getTravelList():
            ac = t.getAirlineCode() if hasattr(t, 'getAirlineCode') else 0
            toc = t.getTourOperatorCode() if hasattr(t, 'getTourOperatorCode') else 0
            mc = t.getManagerCode() if hasattr(t, 'getManagerCode') else 0
            self.getCurs().execute(
                'INSERT OR REPLACE INTO package('
                '  code, date, quantity, discount, '
                '  airline_code, touroperator_code, manager_code) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (t.getCode(), t.getDate(), t.getQuantity(), t.getDiscount(),
                 ac, toc, mc))

    def writeAirlineTable(self):
        for a in self.getLib().getAirlineList():
            self.getCurs().execute(
                'INSERT OR REPLACE INTO airline(code, name, flight_cost) '
                'VALUES (?, ?, ?)',
                (a.getCode(), a.getName(), a.getFlightCost()))

    def writeTourOperatorTable(self):
        for t in self.getLib().getTourOperatorList():
            self.getCurs().execute(
                'INSERT OR REPLACE INTO touroperator('
                '  code, name, address, phone, website) '
                'VALUES (?, ?, ?, ?, ?)',
                (t.getCode(), t.getName(), t.getAddress(),
                 t.getPhone(), t.getWebsite()))

    def writeManagerTable(self):
        for m in self.getLib().getManagerList():
            self.getCurs().execute(
                'INSERT OR REPLACE INTO manager('
                '  code, surname, name, secname, position, phone, email) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (m.getCode(), m.getSurname(), m.getName(), m.getSecname(),
                 m.getPosition(), m.getPhone(), m.getEmail()))

    def writePaymentTable(self):
        for p in self.getLib().getPaymentList():
            self.getCurs().execute(
                'INSERT OR REPLACE INTO payment('
                '  code, package_code, date, amount, method, status) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (p.getCode(), p.getPackageCode(), p.getDate(),
                 p.getAmount(), p.getMethod(), p.getStatus()))
