#!/usr/bin/env python3
"""Генерирует ``demo.xml`` и ``demo.sqlite`` с одинаковым содержимым.

Набор записей соответствует расширенной модели (как у ``demo.json``), но данные
другие. Запуск из корня проекта::

    python data/generate_demo_assets.py

Перед записью SQLite удаляется существующий файл ``demo.sqlite``.
"""

from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'


def _setup_path():
    os.chdir(ROOT)
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))


def build_demo_library():
    from domain.travel_company_ext import TravelCompanyExt

    lib = TravelCompanyExt()

    clients = [
        (1, 'Воробьёв', 'Сергей', 'Николаевич',
         'г. Сочи, ул. Навагинская, д. 9', '+7 (862) 240-11-22'),
        (2, 'Никифорова', 'Татьяна', 'Владимировна',
         'г. Краснодар, ул. Красная, д. 122', '+7 (861) 330-44-55'),
        (3, 'Романов', 'Игорь', 'Станиславович',
         'г. Воронеж, ул. Плехановская, д. 44', '+7 (473) 255-66-77'),
        (4, 'Фёдорова', 'Наталья', 'Евгеньевна',
         'г. Нижний Новгород, ул. Большая Печёрская, д. 18',
         '+7 (831) 422-88-99'),
        (5, 'Гришин', 'Павел', 'Алексеевич',
         'г. Самара, ул. Ленинградская, д. 58', '+7 (846) 311-00-12'),
    ]
    for row in clients:
        lib.create_client(*row)

    routes = [
        (1, 'Испания', 'Средиземноморский', 11,
         'Barceló Marbella 4*', 102000),
        (2, 'Египет', 'Субтропический сухой', 8,
         'Steigenberger Alcazar 5*', 72000),
        (3, 'Кипр', 'Средиземноморский', 7, 'Capo Bay Hotel 4*', 85000),
        (4, 'Вьетнам', 'Тропический муссонный', 10,
         'Vinpearl Resort & Spa 5*', 125000),
        (5, 'Норвегия', 'Умеренный морской', 6,
         'Scandic Ishavshotel 4*', 195000),
    ]
    for row in routes:
        lib.create_route(*row)

    airlines = [
        (1, 'S7 Airlines', 25000),
        (2, 'Qatar Airways', 55000),
        (3, 'Lufthansa', 42000),
        (4, 'Air France', 45000),
    ]
    for row in airlines:
        lib.create_airline(*row)

    touroperators = [
        (1, 'Tez Tour', 'г. Москва, ул. Большая Дмитровка, д. 11',
         '+7 (495) 411-22-33', 'https://www.tez-tour.com'),
        (2, 'Intourist', 'г. Москва, ул. Новый Арбат, д. 36',
         '+7 (495) 988-77-66', 'https://www.intourist.ru'),
        (3, 'Sunmar', 'г. Санкт-Петербург, Лиговский пр-т, д. 10',
         '+7 (812) 448-00-11', 'https://www.sunmar.ru'),
        (4, 'Natalie Tours', 'г. Москва, ул. Стромынка, д. 18',
         '+7 (495) 735-90-90', 'https://natalie-tours.ru'),
    ]
    for row in touroperators:
        lib.create_tour_operator(*row)

    managers = [
        (1, 'Семёнов', 'Пётр', 'Викторович',
         'Руководитель отдела продаж', '+7 (495) 200-20-01',
         'semenov@demo.travel'),
        (2, 'Крылова', 'Светлана', 'Павловна',
         'Ведущий менеджер', '+7 (495) 200-20-02', 'krylova@demo.travel'),
        (3, 'Назаров', 'Руслан', 'Тимурович',
         'Менеджер корпоративных клиентов', '+7 (495) 200-20-03',
         'nazarov@demo.travel'),
    ]
    for row in managers:
        lib.create_manager(*row)

    travels = [
        # code, date, qty, disc, airline, tourop, manager, clients, routes
        (1, '22.04.2026', 2, 3, 2, 1, 1, [1, 2], [1]),
        (2, '10.05.2026', 1, 0, 1, 2, 2, [3], [2]),
        (3, '18.05.2026', 1, 7, 3, 2, 1, [4], [3]),
        (4, '02.06.2026', 2, 5, 1, 3, 3, [2, 5], [4]),
        (5, '20.06.2026', 1, 12, 4, 4, 2, [4], [3, 4]),
    ]
    for (code, date, qty, disc, ac, toc, mc, cl_codes, rt_codes) in travels:
        t = lib.create_travel(code, date, qty, disc, ac, toc, mc)
        for cc in cl_codes:
            t.append_client(cc)
        for rc in rt_codes:
            t.append_route(rc)

    payments = [
        (1, 1, '05.03.2026', 198500, 'карта', 'оплачен'),
        (2, 2, '08.03.2026', 92000, 'перевод', 'оплачен'),
        (3, 3, '12.03.2026', 315900, 'карта', 'в ожидании'),
        (4, 4, '15.03.2026', 248400, 'наличные', 'отменён'),
        (5, 5, '01.04.2026', 182000, 'наличные', 'оплачен'),
    ]
    for row in payments:
        lib.create_payment(*row)

    return lib


def main():
    _setup_path()
    from dataaccess.data_xml_ext import DataXmlExt
    from dataaccess.data_sql_ext import DataSqlExt

    lib = build_demo_library()

    xml_path = DATA / 'demo.xml'
    sql_path = DATA / 'demo.sqlite'

    if sql_path.is_file():
        sql_path.unlink()

    DataXmlExt(lib).write_file(filename=str(xml_path))
    DataSqlExt(lib).write_file(filename=str(sql_path))

    print(f'Записано: {xml_path}')
    print(f'Записано: {sql_path}')


if __name__ == '__main__':
    main()
