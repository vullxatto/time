"""SQLite-сериализация расширенной модели.

Дополняет схему `DataSql` четырьмя новыми таблицами (airline, touroperator,
manager, payment) и тремя FK-колонками в таблице package
(airline_code, touroperator_code, manager_code).
"""

import sqlite3
from dataaccess.data_sql import DataSql


class DataSqlExt(DataSql):
    """Сериализатор расширенной модели в SQLite."""

    # ------------------------------------------------------------------
    # схема
    # ------------------------------------------------------------------
    def create_tables(self):
        super().create_tables()
        # дополняем package колонками-FK; ALTER падает, если столбец уже есть —
        # это нормально при повторной записи в существующий файл.
        for col in ('airline_code', 'touroperator_code', 'manager_code'):
            try:
                self.get_curs().execute(
                    f'ALTER TABLE package ADD COLUMN {col} INTEGER DEFAULT 0')
            except sqlite3.OperationalError:
                pass
        self.create_airline_table()
        self.create_tour_operator_table()
        self.create_manager_table()
        self.create_payment_table()

    def create_airline_table(self):
        self.get_curs().execute('''
            CREATE TABLE IF NOT EXISTS airline (
                code        INTEGER PRIMARY KEY,
                name        TEXT,
                flight_cost INTEGER
            );''')

    def create_tour_operator_table(self):
        self.get_curs().execute('''
            CREATE TABLE IF NOT EXISTS touroperator (
                code    INTEGER PRIMARY KEY,
                name    TEXT,
                address TEXT,
                phone   TEXT,
                website TEXT
            );''')

    def create_manager_table(self):
        self.get_curs().execute('''
            CREATE TABLE IF NOT EXISTS manager (
                code     INTEGER PRIMARY KEY,
                surname  TEXT,
                name     TEXT,
                secname  TEXT,
                position TEXT,
                phone    TEXT,
                email    TEXT
            );''')

    def create_payment_table(self):
        # связь 1:1 с путёвкой обеспечивается UNIQUE на package_code
        self.get_curs().execute('''
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
    def read_tables(self):
        super().read_tables()
        self.read_airline_table()
        self.read_tour_operator_table()
        self.read_manager_table()
        self.read_payment_table()

    def read_package_table(self):
        try:
            self.get_curs().execute(
                'SELECT code, date, quantity, discount, '
                '       COALESCE(airline_code, 0), '
                '       COALESCE(touroperator_code, 0), '
                '       COALESCE(manager_code, 0) '
                'FROM package')
            for r in self.get_curs().fetchall():
                self.get_lib().create_travel(
                    r[0], r[1], r[2], r[3], int(r[4]), int(r[5]), int(r[6]))
        except sqlite3.OperationalError:
            # старая БД без расширенных колонок — fallback на базовую схему
            self.get_curs().execute(
                'SELECT code, date, quantity, discount FROM package')
            for r in self.get_curs().fetchall():
                self.get_lib().create_travel(r[0], r[1], r[2], r[3])

    def read_airline_table(self):
        try:
            self.get_curs().execute('SELECT code, name, flight_cost FROM airline')
            for r in self.get_curs().fetchall():
                self.get_lib().create_airline(r[0], r[1], r[2])
        except sqlite3.OperationalError:
            pass

    def read_tour_operator_table(self):
        try:
            self.get_curs().execute(
                'SELECT code, name, address, phone, website FROM touroperator')
            for r in self.get_curs().fetchall():
                self.get_lib().create_tour_operator(r[0], r[1], r[2], r[3], r[4])
        except sqlite3.OperationalError:
            pass

    def read_manager_table(self):
        try:
            self.get_curs().execute(
                'SELECT code, surname, name, secname, position, phone, email '
                'FROM manager')
            for r in self.get_curs().fetchall():
                self.get_lib().create_manager(
                    r[0], r[1], r[2], r[3], r[4], r[5], r[6])
        except sqlite3.OperationalError:
            pass

    def read_payment_table(self):
        try:
            self.get_curs().execute(
                'SELECT code, package_code, date, amount, method, status '
                'FROM payment')
            for r in self.get_curs().fetchall():
                self.get_lib().create_payment(
                    r[0], r[1], r[2], r[3], r[4], r[5])
        except sqlite3.OperationalError:
            pass

    # ------------------------------------------------------------------
    # запись
    # ------------------------------------------------------------------
    def write_tables(self):
        super().write_tables()
        self.write_airline_table()
        self.write_tour_operator_table()
        self.write_manager_table()
        self.write_payment_table()

    def write_package_table(self):
        # переопределяем, чтобы записать дополнительные FK-колонки
        for t in self.get_lib().get_travel_list():
            ac = t.get_airline_code() if hasattr(t, 'get_airline_code') else 0
            toc = t.get_tour_operator_code() if hasattr(t, 'get_tour_operator_code') else 0
            mc = t.get_manager_code() if hasattr(t, 'get_manager_code') else 0
            self.get_curs().execute(
                'INSERT OR REPLACE INTO package('
                '  code, date, quantity, discount, '
                '  airline_code, touroperator_code, manager_code) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (t.get_code(), t.get_date(), t.get_quantity(), t.get_discount(),
                 ac, toc, mc))

    def write_airline_table(self):
        for a in self.get_lib().get_airline_list():
            self.get_curs().execute(
                'INSERT OR REPLACE INTO airline(code, name, flight_cost) '
                'VALUES (?, ?, ?)',
                (a.get_code(), a.get_name(), a.get_flight_cost()))

    def write_tour_operator_table(self):
        for t in self.get_lib().get_tour_operator_list():
            self.get_curs().execute(
                'INSERT OR REPLACE INTO touroperator('
                '  code, name, address, phone, website) '
                'VALUES (?, ?, ?, ?, ?)',
                (t.get_code(), t.get_name(), t.get_address(),
                 t.get_phone(), t.get_website()))

    def write_manager_table(self):
        for m in self.get_lib().get_manager_list():
            self.get_curs().execute(
                'INSERT OR REPLACE INTO manager('
                '  code, surname, name, secname, position, phone, email) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (m.get_code(), m.get_surname(), m.get_name(), m.get_secname(),
                 m.get_position(), m.get_phone(), m.get_email()))

    def write_payment_table(self):
        for p in self.get_lib().get_payment_list():
            self.get_curs().execute(
                'INSERT OR REPLACE INTO payment('
                '  code, package_code, date, amount, method, status) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (p.get_code(), p.get_package_code(), p.get_date(),
                 p.get_amount(), p.get_method(), p.get_status()))
