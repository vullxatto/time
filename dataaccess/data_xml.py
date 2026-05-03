"""Чтение/запись данных в XML (3 базовые сущности)."""

import xml.dom.minidom
from dataaccess.data import Data


class DataXml(Data):

    def read(self):
        dom = xml.dom.minidom.parse(self.get_inp())
        dom.normalize()
        root = dom.documentElement
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            if node.nodeName == 'clients':
                self.read_clients(node)
            elif node.nodeName == 'routes':
                self.read_routes(node)
            elif node.nodeName == 'travels':
                self.read_travels(node)

    def read_clients(self, node):
        for cl in node.getElementsByTagName('client'):
            self.get_lib().create_client(
                int(cl.getAttribute('code') or 0),
                cl.getAttribute('surname') or '',
                cl.getAttribute('name') or '',
                cl.getAttribute('secname') or '',
                cl.getAttribute('address') or '',
                cl.getAttribute('phone') or '',
            )

    def read_routes(self, node):
        for rt in node.getElementsByTagName('route'):
            self.get_lib().create_route(
                int(rt.getAttribute('code') or 0),
                rt.getAttribute('name') or '',
                rt.getAttribute('climate') or '',
                int(rt.getAttribute('duration') or 0),
                rt.getAttribute('hotel') or '',
                int(rt.getAttribute('cost') or 0),
            )

    def read_travels(self, node):
        for tr in node.getElementsByTagName('travel'):
            travel = self.get_lib().create_travel(
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
                            travel.append_client(cc)
                elif child.nodeName == 'routes':
                    for r in child.getElementsByTagName('route'):
                        rc = int(r.getAttribute('code') or 0)
                        if rc:
                            travel.append_route(rc)

    def write(self):
        dom = xml.dom.minidom.Document()
        root = dom.createElement('travelcompany')
        dom.appendChild(root)
        self._write_clients(dom, root)
        self._write_routes(dom, root)
        self._write_travels(dom, root)
        with open(self.get_out(), 'w', encoding='utf-8') as f:
            f.write(dom.toprettyxml(indent='  '))

    def _write_clients(self, dom, root):
        clients = dom.createElement('clients')
        root.appendChild(clients)
        for c in self.get_lib().get_client_list():
            cl = dom.createElement('client')
            cl.setAttribute('code', str(c.get_code()))
            cl.setAttribute('surname', c.get_surname() or '')
            cl.setAttribute('name', c.get_name() or '')
            cl.setAttribute('secname', c.get_secname() or '')
            cl.setAttribute('address', c.get_address() or '')
            cl.setAttribute('phone', c.get_phone() or '')
            clients.appendChild(cl)

    def _write_routes(self, dom, root):
        routes = dom.createElement('routes')
        root.appendChild(routes)
        for r in self.get_lib().get_route_list():
            rt = dom.createElement('route')
            rt.setAttribute('code', str(r.get_code()))
            rt.setAttribute('name', r.get_name() or '')
            rt.setAttribute('climate', r.get_climate() or '')
            rt.setAttribute('duration', str(r.get_duration()))
            rt.setAttribute('hotel', r.get_hotel() or '')
            rt.setAttribute('cost', str(r.get_cost()))
            routes.appendChild(rt)

    def _write_travels(self, dom, root):
        travels = dom.createElement('travels')
        root.appendChild(travels)
        for t in self.get_lib().get_travel_list():
            tr = dom.createElement('travel')
            tr.setAttribute('code', str(t.get_code()))
            tr.setAttribute('date', t.get_date() or '')
            tr.setAttribute('quantity', str(t.get_quantity()))
            tr.setAttribute('discount', str(t.get_discount()))
            cl_elem = dom.createElement('clients')
            for code in t.get_client_codes():
                c = dom.createElement('client')
                c.setAttribute('code', str(code))
                cl_elem.appendChild(c)
            tr.appendChild(cl_elem)
            rt_elem = dom.createElement('routes')
            for code in t.get_route_codes():
                r = dom.createElement('route')
                r.setAttribute('code', str(code))
                rt_elem.appendChild(r)
            tr.appendChild(rt_elem)
            travels.appendChild(tr)
