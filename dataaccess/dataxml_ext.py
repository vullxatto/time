import xml.dom.minidom
from dataxml import dataxml

class dataxml_ext(dataxml):

    def read(self):
        super().read()
        self.patch_travel_airline_touroperator_from_xml()
        dom = xml.dom.minidom.parse(self.getInp())
        root = dom.documentElement
        for node in root.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.nodeName == 'airlines':
                    self.readAirlines(node)
                elif node.nodeName == 'touroperators':
                    self.readTourOperators(node)

    def patch_travel_airline_touroperator_from_xml(self):
        dom = xml.dom.minidom.parse(self.getInp())
        root = dom.documentElement
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE or node.nodeName != 'travels':
                continue
            for tr in node.getElementsByTagName('travel'):
                code = int(tr.getAttribute('code') or 0)
                ac = int(tr.getAttribute('airline_code') or 0)
                tc = int(tr.getAttribute('touroperator_code') or 0)
                t = self.getLib().getTravel(code)
                if t and hasattr(t, 'setAirlineCode'):
                    t.setAirlineCode(ac)
                    t.setTourOperatorCode(tc)

    def readAirlines(self, node):
        for a in node.getElementsByTagName('airline'):
            code = int(a.getAttribute('code') or 0)
            name = a.getAttribute('name') or ''
            fc = a.getAttribute('flight_cost')
            if fc == '':
                c = a.getAttribute('country') or '0'
                try:
                    fc = int(c) if str(c).strip().isdigit() else 0
                except (TypeError, ValueError):
                    fc = 0
            else:
                try:
                    fc = int(fc)
                except (TypeError, ValueError):
                    fc = 0
            self.getLib().createAirline(code, name, fc)

    def readTourOperators(self, node):
        for t in node.getElementsByTagName('touroperator'):
            code = int(t.getAttribute('code') or 0)
            name = t.getAttribute('name') or ''
            address = t.getAttribute('address') or ''
            phone = t.getAttribute('phone') or ''
            website = t.getAttribute('website') or ''
            self.getLib().createTourOperator(code, name, address, phone, website)

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
            if hasattr(t, 'getAirlineCode'):
                tr.setAttribute('airline_code', str(t.getAirlineCode()))
                tr.setAttribute('touroperator_code', str(t.getTourOperatorCode()))
            else:
                tr.setAttribute('airline_code', '0')
                tr.setAttribute('touroperator_code', '0')
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
        airlines_el = dom.createElement('airlines')
        root.appendChild(airlines_el)
        for a in self.getLib().getAirlineList():
            al = dom.createElement('airline')
            al.setAttribute('code', str(a.getCode()))
            al.setAttribute('name', a.getName() or '')
            al.setAttribute('flight_cost', str(a.getFlightCost()))
            airlines_el.appendChild(al)
        tourops_el = dom.createElement('touroperators')
        root.appendChild(tourops_el)
        for op in self.getLib().getTourOperatorList():
            te = dom.createElement('touroperator')
            te.setAttribute('code', str(op.getCode()))
            te.setAttribute('name', op.getName() or '')
            te.setAttribute('address', op.getAddress() or '')
            te.setAttribute('phone', op.getPhone() or '')
            te.setAttribute('website', op.getWebsite() or '')
            tourops_el.appendChild(te)
        with open(self.getOut(), 'w', encoding='utf-8') as f:
            f.write(dom.toprettyxml(indent='  '))
