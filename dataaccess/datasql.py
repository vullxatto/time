import sqlite3 as db
from dataaccess.data import data

class datasql(data):

    def getCurs(self):
        return self.__curs

    def read(self):
        self.__conn = db.connect(self.getInp())
        self.__curs = self.__conn.cursor()
        self.readTables()
        self.__conn.close()

    def write(self):
        self.__conn = db.connect(self.getOut())
        self.__curs = self.__conn.cursor()
        self.createTables()
        self.writeTables()
        self.__conn.commit()
        self.__conn.close()

    def createTables(self):
        self.createClientTable()
        self.createRoutesTable()
        self.createPackageTable()
        self.createPackageClientTable()
        self.createPackageRouteTable()

    def createClientTable(self):
        self.getCurs().execute('\n            create table client\n            (code integer primary key,\n            surname text,\n            name text,\n            secname text,\n            address text,\n            phone text);')

    def createRoutesTable(self):
        self.getCurs().execute('\n            create table routes\n            (code integer primary key,\n            name text,\n            climate text,\n            duration integer,\n            hotel text,\n            cost integer);')

    def createPackageTable(self):
        self.getCurs().execute('\n            create table package\n            (code integer primary key,\n            date text,\n            quantity integer,\n            discount integer);')

    def createPackageClientTable(self):
        self.getCurs().execute('\n            create table package_client\n            (code integer primary key autoincrement,\n            package integer references package(code) on update cascade on delete cascade,\n            client integer references client(code) on update cascade on delete cascade,\n            unique(package, client));')

    def createPackageRouteTable(self):
        self.getCurs().execute('\n            create table package_route\n            (code integer primary key autoincrement,\n            package integer references package(code) on update cascade on delete cascade,\n            routes integer references routes(code) on update cascade on delete cascade,\n            unique(package, routes));')

    def readTables(self):
        self.readClientTable()
        self.readRoutesTable()
        self.readPackageTable()
        self.readPackageClientTable()
        self.readPackageRouteTable()

    def readClientTable(self):
        self.getCurs().execute('select code,surname,name,secname,address,phone from client')
        data = self.getCurs().fetchall()
        for r in data:
            self.getLib().createClient(r[0], r[1], r[2], r[3], r[4], r[5])

    def readRoutesTable(self):
        self.getCurs().execute('select code,name,climate,duration,hotel,cost from routes')
        data = self.getCurs().fetchall()
        for r in data:
            self.getLib().createRoute(r[0], r[1], r[2], r[3], r[4], r[5])

    def readPackageTable(self):
        self.getCurs().execute('select code,date,quantity,discount from package')
        data = self.getCurs().fetchall()
        for r in data:
            self.getLib().createTravel(r[0], r[1], r[2], r[3])

    def readPackageClientTable(self):
        self.getCurs().execute('select package,client from package_client')
        data = self.getCurs().fetchall()
        for r in data:
            travel = self.getLib().getTravel(r[0])
            client = self.getLib().getClient(r[1])
            if travel and client:
                travel.appendClient(client)

    def readPackageRouteTable(self):
        self.getCurs().execute('select package,routes from package_route')
        data = self.getCurs().fetchall()
        for r in data:
            travel = self.getLib().getTravel(r[0])
            route = self.getLib().getRoute(r[1])
            if travel and route:
                travel.appendRoute(route)

    def writeTables(self):
        self.writeClientTable()
        self.writeRoutesTable()
        self.writePackageTable()
        self.writePackageClientTable()
        self.writePackageRouteTable()

    def writeClientTable(self):
        for c in self.getLib().getClientList():
            self.getCurs().execute(f"insert into client(code,surname,name,secname,address,phone) values('{c.getCode()}','{c.getSurname()}','{c.getName()}','{c.getSecname()}','{c.getAddress()}','{c.getPhone()}')")

    def writeRoutesTable(self):
        for r in self.getLib().getRouteList():
            self.getCurs().execute(f"insert into routes(code,name,climate,duration,hotel,cost) values('{r.getCode()}','{r.getName()}','{r.getClimate()}','{r.getDuration()}','{r.getHotel()}','{r.getCost()}')")

    def writePackageTable(self):
        for t in self.getLib().getTravelList():
            self.getCurs().execute(f"insert into package(code,date,quantity,discount) values('{t.getCode()}','{t.getDate()}','{t.getQuantity()}','{t.getDiscount()}')")

    def writePackageClientTable(self):
        for t in self.getLib().getTravelList():
            for cl in t.getClientCodes():
                self.getCurs().execute(f"insert into package_client(package,client) values('{t.getCode()}','{cl}')")

    def writePackageRouteTable(self):
        for t in self.getLib().getTravelList():
            for rt in t.getRouteCodes():
                self.getCurs().execute(f"insert into package_route(package,routes) values('{t.getCode()}','{rt}')")
