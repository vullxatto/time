import xml.dom.minidom
from dataaccess.data import data

class dataxml(data):

    def read(self):
        dom = xml.dom.minidom.parse(self.getInp())
        dom.normalize()
        root = dom.childNodes[0]
        for node in root.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.nodeName == 'clients':
                    self.readClients(node)
                elif node.nodeName == 'routes':
                    self.readRoutes(node)
                elif node.nodeName == 'travels':
                    self.readTravels(node)

    def readClients(self, node):
        for cl in node.getElementsByTagName('client'):
            code = int(cl.getAttribute('code') or 0)
            surname = cl.getAttribute('surname') or ''
            name = cl.getAttribute('name') or ''
            secname = cl.getAttribute('secname') or ''
            address = cl.getAttribute('address') or ''
            phone = cl.getAttribute('phone') or ''
            self.getLib().createClient(code, surname, name, secname, address, phone)

    def readRoutes(self, node):
        for rt in node.getElementsByTagName('route'):
            code = int(rt.getAttribute('code') or 0)
            name = rt.getAttribute('name') or ''
            climate = rt.getAttribute('climate') or ''
            duration = int(rt.getAttribute('duration') or 0)
            hotel = rt.getAttribute('hotel') or ''
            cost = int(rt.getAttribute('cost') or 0)
            self.getLib().createRoute(code, name, climate, duration, hotel, cost)

    def readTravels(self, node):
        for tr in node.getElementsByTagName('travel'):
            code = int(tr.getAttribute('code') or 0)
            date = tr.getAttribute('date') or ''
            quantity = int(tr.getAttribute('quantity') or 0)
            discount = int(tr.getAttribute('discount') or 0)
            travel = self.getLib().createTravel(code, date, quantity, discount)
            for c in tr.getElementsByTagName('client'):
                client_code = int(c.getAttribute('code') or 0)
                if client_code:
                    travel.appendClient(client_code)
            for r in tr.getElementsByTagName('route'):
                route_code = int(r.getAttribute('code') or 0)
                if route_code:
                    travel.appendRoute(route_code)

    def write(self):
        dom = xml.dom.minidom.Document()
        root = dom.createElement('travelcompany')
        dom.appendChild(root)
        clients = dom.createElement('clients')
        root.appendChild(clients)
        for c in self.getLib().getClientList():
            cl = dom.createElement('client')
            cl.setAttribute('code', str(c.getCode()))
            cl.setAttribute('surname', c.getSurname() or '')
            cl.setAttribute('name', c.getName() or '')
            cl.setAttribute('secname', c.getSecname() or '')
            cl.setAttribute('address', c.getAddress() or '')
            cl.setAttribute('phone', c.getPhone() or '')
            clients.appendChild(cl)
        routes = dom.createElement('routes')
        root.appendChild(routes)
        for r in self.getLib().getRouteList():
            rt = dom.createElement('route')
            rt.setAttribute('code', str(r.getCode()))
            rt.setAttribute('name', r.getName() or '')
            rt.setAttribute('climate', r.getClimate() or '')
            rt.setAttribute('duration', str(r.getDuration()))
            rt.setAttribute('hotel', r.getHotel() or '')
            rt.setAttribute('cost', str(r.getCost()))
            routes.appendChild(rt)
        travels = dom.createElement('travels')
        root.appendChild(travels)
        for t in self.getLib().getTravelList():
            tr = dom.createElement('travel')
            tr.setAttribute('code', str(t.getCode()))
            tr.setAttribute('date', t.getDate() or '')
            tr.setAttribute('quantity', str(t.getQuantity()))
            tr.setAttribute('discount', str(t.getDiscount()))
            cl_elem = dom.createElement('clients')
            for code in t.getClientCodes():
                c = dom.createElement('client')
                c.setAttribute('code', str(code))
                cl_elem.appendChild(c)
            tr.appendChild(cl_elem)
            rt_elem = dom.createElement('routes')
            for code in t.getRouteCodes():
                r = dom.createElement('route')
                r.setAttribute('code', str(code))
                rt_elem.appendChild(r)
            tr.appendChild(rt_elem)
            travels.appendChild(tr)
        with open(self.getOut(), 'w', encoding='utf-8') as f:
            f.write(dom.toprettyxml(indent='  '))

    def readFile(self, filename=''):
        if filename:
            self.setInp(filename)
        self.read()

    def writeFile(self, filename=''):
        if filename:
            self.setOut(filename)
        self.write()
