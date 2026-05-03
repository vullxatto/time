"""Расширенный XML-сериализатор: добавляет авиа, туроп, менеджеров, платежи."""

import xml.dom.minidom
from dataaccess.data_xml import DataXml


class DataXmlExt(DataXml):

    def read(self):
        super().read()
        # после базового чтения дозаполняем FK путёвок и читаем новые секции
        dom = xml.dom.minidom.parse(self.get_inp())
        root = dom.documentElement
        self._patch_travel_fk(root)
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            if node.nodeName == 'airlines':
                self._read_airlines(node)
            elif node.nodeName == 'touroperators':
                self._read_tour_operators(node)
            elif node.nodeName == 'managers':
                self._read_managers(node)
            elif node.nodeName == 'payments':
                self._read_payments(node)

    def _patch_travel_fk(self, root):
        """Дозаполняет airline_code/touroperator_code/manager_code у уже созданных путёвок."""
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE or node.nodeName != 'travels':
                continue
            for tr in node.getElementsByTagName('travel'):
                code = int(tr.getAttribute('code') or 0)
                t = self.get_lib().get_travel(code)
                if t is None:
                    continue
                if hasattr(t, 'set_airline_code'):
                    t.set_airline_code(int(tr.getAttribute('airline_code') or 0))
                if hasattr(t, 'set_tour_operator_code'):
                    t.set_tour_operator_code(int(tr.getAttribute('touroperator_code') or 0))
                if hasattr(t, 'set_manager_code'):
                    t.set_manager_code(int(tr.getAttribute('manager_code') or 0))

    def _read_airlines(self, node):
        for a in node.getElementsByTagName('airline'):
            try:
                fc = int(a.getAttribute('flight_cost') or 0)
            except (TypeError, ValueError):
                fc = 0
            self.get_lib().create_airline(
                int(a.getAttribute('code') or 0),
                a.getAttribute('name') or '',
                fc,
            )

    def _read_tour_operators(self, node):
        for t in node.getElementsByTagName('touroperator'):
            self.get_lib().create_tour_operator(
                int(t.getAttribute('code') or 0),
                t.getAttribute('name') or '',
                t.getAttribute('address') or '',
                t.getAttribute('phone') or '',
                t.getAttribute('website') or '',
            )

    def _read_managers(self, node):
        for m in node.getElementsByTagName('manager'):
            self.get_lib().create_manager(
                int(m.getAttribute('code') or 0),
                m.getAttribute('surname') or '',
                m.getAttribute('name') or '',
                m.getAttribute('secname') or '',
                m.getAttribute('position') or '',
                m.getAttribute('phone') or '',
                m.getAttribute('email') or '',
            )

    def _read_payments(self, node):
        for p in node.getElementsByTagName('payment'):
            try:
                amount = int(p.getAttribute('amount') or 0)
            except (TypeError, ValueError):
                amount = 0
            self.get_lib().create_payment(
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
        self._write_clients(dom, root)
        self._write_routes(dom, root)
        self._write_travels_ext(dom, root)
        # новые секции
        self._write_airlines(dom, root)
        self._write_tour_operators(dom, root)
        self._write_managers(dom, root)
        self._write_payments(dom, root)
        with open(self.get_out(), 'w', encoding='utf-8') as f:
            f.write(dom.toprettyxml(indent='  '))

    def _write_travels_ext(self, dom, root):
        travels = dom.createElement('travels')
        root.appendChild(travels)
        for t in self.get_lib().get_travel_list():
            tr = dom.createElement('travel')
            tr.setAttribute('code', str(t.get_code()))
            tr.setAttribute('date', t.get_date() or '')
            tr.setAttribute('quantity', str(t.get_quantity()))
            tr.setAttribute('discount', str(t.get_discount()))
            tr.setAttribute('airline_code', str(t.get_airline_code() if hasattr(t, 'get_airline_code') else 0))
            tr.setAttribute('touroperator_code', str(t.get_tour_operator_code() if hasattr(t, 'get_tour_operator_code') else 0))
            tr.setAttribute('manager_code', str(t.get_manager_code() if hasattr(t, 'get_manager_code') else 0))
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

    def _write_airlines(self, dom, root):
        airlines_el = dom.createElement('airlines')
        root.appendChild(airlines_el)
        for a in self.get_lib().get_airline_list():
            al = dom.createElement('airline')
            al.setAttribute('code', str(a.get_code()))
            al.setAttribute('name', a.get_name() or '')
            al.setAttribute('flight_cost', str(a.get_flight_cost()))
            airlines_el.appendChild(al)

    def _write_tour_operators(self, dom, root):
        ops_el = dom.createElement('touroperators')
        root.appendChild(ops_el)
        for op in self.get_lib().get_tour_operator_list():
            te = dom.createElement('touroperator')
            te.setAttribute('code', str(op.get_code()))
            te.setAttribute('name', op.get_name() or '')
            te.setAttribute('address', op.get_address() or '')
            te.setAttribute('phone', op.get_phone() or '')
            te.setAttribute('website', op.get_website() or '')
            ops_el.appendChild(te)

    def _write_managers(self, dom, root):
        mgrs_el = dom.createElement('managers')
        root.appendChild(mgrs_el)
        for m in self.get_lib().get_manager_list():
            me = dom.createElement('manager')
            me.setAttribute('code', str(m.get_code()))
            me.setAttribute('surname', m.get_surname() or '')
            me.setAttribute('name', m.get_name() or '')
            me.setAttribute('secname', m.get_secname() or '')
            me.setAttribute('position', m.get_position() or '')
            me.setAttribute('phone', m.get_phone() or '')
            me.setAttribute('email', m.get_email() or '')
            mgrs_el.appendChild(me)

    def _write_payments(self, dom, root):
        pays_el = dom.createElement('payments')
        root.appendChild(pays_el)
        for p in self.get_lib().get_payment_list():
            pe = dom.createElement('payment')
            pe.setAttribute('code', str(p.get_code()))
            pe.setAttribute('package_code', str(p.get_package_code()))
            pe.setAttribute('date', p.get_date() or '')
            pe.setAttribute('amount', str(p.get_amount()))
            pe.setAttribute('method', p.get_method() or '')
            pe.setAttribute('status', p.get_status() or '')
            pays_el.appendChild(pe)
