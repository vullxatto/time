"""Расширенный XML-сериализатор: добавляет авиа, туроп, менеджеров, платежи."""

import xml.dom.minidom
from dataaccess.dataxml import dataxml


class dataxml_ext(dataxml):

    def read(self):
        super().read()
        # после базового чтения дозаполняем FK путёвок и читаем новые секции
        dom = xml.dom.minidom.parse(self.getInp())
        root = dom.documentElement
        self._patch_travel_fk(root)
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            if node.nodeName == 'airlines':
                self._readAirlines(node)
            elif node.nodeName == 'touroperators':
                self._readTourOperators(node)
            elif node.nodeName == 'managers':
                self._readManagers(node)
            elif node.nodeName == 'payments':
                self._readPayments(node)

    def _patch_travel_fk(self, root):
        """Дозаполняет airline_code/touroperator_code/manager_code у уже созданных путёвок."""
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE or node.nodeName != 'travels':
                continue
            for tr in node.getElementsByTagName('travel'):
                code = int(tr.getAttribute('code') or 0)
                t = self.getLib().getTravel(code)
                if t is None:
                    continue
                if hasattr(t, 'setAirlineCode'):
                    t.setAirlineCode(int(tr.getAttribute('airline_code') or 0))
                if hasattr(t, 'setTourOperatorCode'):
                    t.setTourOperatorCode(int(tr.getAttribute('touroperator_code') or 0))
                if hasattr(t, 'setManagerCode'):
                    t.setManagerCode(int(tr.getAttribute('manager_code') or 0))

    def _readAirlines(self, node):
        for a in node.getElementsByTagName('airline'):
            try:
                fc = int(a.getAttribute('flight_cost') or 0)
            except (TypeError, ValueError):
                fc = 0
            self.getLib().createAirline(
                int(a.getAttribute('code') or 0),
                a.getAttribute('name') or '',
                fc,
            )

    def _readTourOperators(self, node):
        for t in node.getElementsByTagName('touroperator'):
            self.getLib().createTourOperator(
                int(t.getAttribute('code') or 0),
                t.getAttribute('name') or '',
                t.getAttribute('address') or '',
                t.getAttribute('phone') or '',
                t.getAttribute('website') or '',
            )

    def _readManagers(self, node):
        for m in node.getElementsByTagName('manager'):
            self.getLib().createManager(
                int(m.getAttribute('code') or 0),
                m.getAttribute('surname') or '',
                m.getAttribute('name') or '',
                m.getAttribute('secname') or '',
                m.getAttribute('position') or '',
                m.getAttribute('phone') or '',
                m.getAttribute('email') or '',
            )

    def _readPayments(self, node):
        for p in node.getElementsByTagName('payment'):
            try:
                amount = int(p.getAttribute('amount') or 0)
            except (TypeError, ValueError):
                amount = 0
            self.getLib().createPayment(
                int(p.getAttribute('code') or 0),
                int(p.getAttribute('package_code') or 0),
                p.getAttribute('date') or '',
                amount,
                p.getAttribute('method') or '',
                p.getAttribute('status') or 'в ожидании',
            )

    def write(self):
        dom = xml.dom.minidom.Document()
        root = dom.createElement('travelcompany')
        dom.appendChild(root)
        # унаследованные секции
        self._writeClients(dom, root)
        self._writeRoutes(dom, root)
        self._writeTravelsExt(dom, root)
        # новые секции
        self._writeAirlines(dom, root)
        self._writeTourOperators(dom, root)
        self._writeManagers(dom, root)
        self._writePayments(dom, root)
        with open(self.getOut(), 'w', encoding='utf-8') as f:
            f.write(dom.toprettyxml(indent='  '))

    def _writeTravelsExt(self, dom, root):
        travels = dom.createElement('travels')
        root.appendChild(travels)
        for t in self.getLib().getTravelList():
            tr = dom.createElement('travel')
            tr.setAttribute('code', str(t.getCode()))
            tr.setAttribute('date', t.getDate() or '')
            tr.setAttribute('quantity', str(t.getQuantity()))
            tr.setAttribute('discount', str(t.getDiscount()))
            tr.setAttribute('airline_code', str(t.getAirlineCode() if hasattr(t, 'getAirlineCode') else 0))
            tr.setAttribute('touroperator_code', str(t.getTourOperatorCode() if hasattr(t, 'getTourOperatorCode') else 0))
            tr.setAttribute('manager_code', str(t.getManagerCode() if hasattr(t, 'getManagerCode') else 0))
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

    def _writeAirlines(self, dom, root):
        airlines_el = dom.createElement('airlines')
        root.appendChild(airlines_el)
        for a in self.getLib().getAirlineList():
            al = dom.createElement('airline')
            al.setAttribute('code', str(a.getCode()))
            al.setAttribute('name', a.getName() or '')
            al.setAttribute('flight_cost', str(a.getFlightCost()))
            airlines_el.appendChild(al)

    def _writeTourOperators(self, dom, root):
        ops_el = dom.createElement('touroperators')
        root.appendChild(ops_el)
        for op in self.getLib().getTourOperatorList():
            te = dom.createElement('touroperator')
            te.setAttribute('code', str(op.getCode()))
            te.setAttribute('name', op.getName() or '')
            te.setAttribute('address', op.getAddress() or '')
            te.setAttribute('phone', op.getPhone() or '')
            te.setAttribute('website', op.getWebsite() or '')
            ops_el.appendChild(te)

    def _writeManagers(self, dom, root):
        mgrs_el = dom.createElement('managers')
        root.appendChild(mgrs_el)
        for m in self.getLib().getManagerList():
            me = dom.createElement('manager')
            me.setAttribute('code', str(m.getCode()))
            me.setAttribute('surname', m.getSurname() or '')
            me.setAttribute('name', m.getName() or '')
            me.setAttribute('secname', m.getSecname() or '')
            me.setAttribute('position', m.getPosition() or '')
            me.setAttribute('phone', m.getPhone() or '')
            me.setAttribute('email', m.getEmail() or '')
            mgrs_el.appendChild(me)

    def _writePayments(self, dom, root):
        pays_el = dom.createElement('payments')
        root.appendChild(pays_el)
        for p in self.getLib().getPaymentList():
            pe = dom.createElement('payment')
            pe.setAttribute('code', str(p.getCode()))
            pe.setAttribute('package_code', str(p.getPackageCode()))
            pe.setAttribute('date', p.getDate() or '')
            pe.setAttribute('amount', str(p.getAmount()))
            pe.setAttribute('method', p.getMethod() or '')
            pe.setAttribute('status', p.getStatus() or '')
            pays_el.appendChild(pe)
