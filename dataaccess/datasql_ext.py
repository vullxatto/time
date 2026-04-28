import sqlite3
from datasql import datasql

class datasql_ext(datasql):

    def createTables(self):
        super().createTables()
        try:
            self.getCurs().execute('ALTER TABLE package ADD COLUMN airline_code INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass
        try:
            self.getCurs().execute('ALTER TABLE package ADD COLUMN touroperator_code INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass
        self.createAirlineTable()
        self.createTourOperatorTable()

    def createAirlineTable(self):
        self.getCurs().execute('\n            CREATE TABLE IF NOT EXISTS airline (\n                code INTEGER PRIMARY KEY,\n                name TEXT,\n                flight_cost INTEGER\n            );')

    def createTourOperatorTable(self):
        self.getCurs().execute('\n            CREATE TABLE IF NOT EXISTS touroperator (\n                code INTEGER PRIMARY KEY,\n                name TEXT,\n                address TEXT,\n                phone TEXT,\n                website TEXT\n            );')

    def readTables(self):
        super().readTables()
        self.readAirlineTable()
        self.readTourOperatorTable()

    def readPackageTable(self):
        try:
            self.getCurs().execute('SELECT code, date, quantity, discount,\n                          COALESCE(airline_code, 0), COALESCE(touroperator_code, 0)\n                   FROM package')
            for r in self.getCurs().fetchall():
                self.getLib().createTravel(r[0], r[1], r[2], r[3], int(r[4]), int(r[5]))
        except sqlite3.OperationalError:
            self.getCurs().execute('SELECT code, date, quantity, discount FROM package')
            for r in self.getCurs().fetchall():
                self.getLib().createTravel(r[0], r[1], r[2], r[3])

    def readAirlineTable(self):
        try:
            self.getCurs().execute('SELECT code, name, flight_cost FROM airline')
            for r in self.getCurs().fetchall():
                self.getLib().createAirline(r[0], r[1], r[2])
        except sqlite3.OperationalError:
            try:
                self.getCurs().execute('SELECT code, name, country, contact FROM airline')
                for r in self.getCurs().fetchall():
                    fc = 0
                    try:
                        if r[2] and str(r[2]).strip().isdigit():
                            fc = int(r[2])
                    except (TypeError, ValueError):
                        fc = 0
                    self.getLib().createAirline(r[0], r[1], fc)
            except sqlite3.OperationalError:
                pass

    def readTourOperatorTable(self):
        try:
            self.getCurs().execute('SELECT code, name, address, phone, website FROM touroperator')
            for r in self.getCurs().fetchall():
                self.getLib().createTourOperator(r[0], r[1], r[2], r[3], r[4])
        except sqlite3.OperationalError:
            pass

    def writeTables(self):
        super().writeTables()
        self.writeAirlineTable()
        self.writeTourOperatorTable()

    def writePackageTable(self):
        for t in self.getLib().getTravelList():
            ac = t.getAirlineCode() if hasattr(t, 'getAirlineCode') else 0
            toc = t.getTourOperatorCode() if hasattr(t, 'getTourOperatorCode') else 0
            self.getCurs().execute('INSERT OR REPLACE INTO package(\n                       code, date, quantity, discount, airline_code, touroperator_code)\n                   VALUES (?, ?, ?, ?, ?, ?)', (t.getCode(), t.getDate(), t.getQuantity(), t.getDiscount(), ac, toc))

    def writeAirlineTable(self):
        for a in self.getLib().getAirlineList():
            self.getCurs().execute('INSERT OR REPLACE INTO airline(code, name, flight_cost)\n                   VALUES (?, ?, ?)', (a.getCode(), a.getName(), a.getFlightCost()))

    def writeTourOperatorTable(self):
        for t in self.getLib().getTourOperatorList():
            self.getCurs().execute('INSERT OR REPLACE INTO touroperator(\n                       code, name, address, phone, website)\n                   VALUES (?, ?, ?, ?, ?)', (t.getCode(), t.getName(), t.getAddress(), t.getPhone(), t.getWebsite()))
