"""Чтение/запись данных в XML (3 базовые сущности)."""

import xml.dom.minidom
from dataaccess.data import data


class dataxml(data):

    def read(self):
        dom = xml.dom.minidom.parse(self.getInp())
        dom.normalize()
        root = dom.documentElement
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            if node.nodeName == 'clients':
                self.readClients(node)
            elif node.nodeName == 'routes':
                self.readRoutes(node)
            elif node.nodeName == 'travels':
                self.readTravels(node)

    def readClients(self, node):
        for cl in node.getElementsByTagName('client'):
            self.getLib().createClient(
                int(cl.getAttribute('code') or 0),
                cl.getAttribute('surname') or '',
                cl.getAttribute('name') or '',
                cl.getAttribute('secname') or '',
                cl.getAttribute('address') or '',
                cl.getAttribute('phone') or '',
            )

    def readRoutes(self, node):
        for rt in node.getElementsByTagName('route'):
            self.getLib().createRoute(
                int(rt.getAttribute('code') or 0),
                rt.getAttribute('name') or '',
                rt.getAttribute('climate') or '',
                int(rt.getAttribute('duration') or 0),
                rt.getAttribute('hotel') or '',
                int(rt.getAttribute('cost') or 0),
            )

    def readTravels(self, node):
        for tr in node.getElementsByTagName('travel'):
            travel = self.getLib().createTravel(
                int(tr.getAttribute('code') or 0),
                tr.getAttribute('date') or '',
                int(tr.getAttribute('quantity') or 0),
                int(tr.getAttribute('discount') or 0),
            )
            if travel is None:
                continue
            # Берём только прямых детей, чтобы не подхватить вложенные client/route
            for child in tr.childNodes:
                if child.nodeType != child.ELEMENT_NODE:
                    continue
                if child.nodeName == 'clients':
                    for c in child.getElementsByTagName('client'):
                        cc = int(c.getAttribute('code') or 0)
                        if cc:
                            travel.appendClient(cc)
                elif child.nodeName == 'routes':
                    for r in child.getElementsByTagName('route'):
                        rc = int(r.getAttribute('code') or 0)
                        if rc:
                            travel.appendRoute(rc)

    def write(self):
        dom = xml.dom.minidom.Document()
        root = dom.createElement('travelcompany')
        dom.appendChild(root)
        self._writeClients(dom, root)
        self._writeRoutes(dom, root)
        self._writeTravels(dom, root)
        with open(self.getOut(), 'w', encoding='utf-8') as f:
            f.write(dom.toprettyxml(indent='  '))

    def _writeClients(self, dom, root):
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

    def _writeRoutes(self, dom, root):
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

    def _writeTravels(self, dom, root):
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
