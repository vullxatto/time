# Информационная система туристической фирмы

Веб-приложение для учёта работы туристической компании: клиенты, маршруты,
путёвки, авиаперевозчики, туроператоры, менеджеры и платежи. Поддерживает
сохранение модели в трёх форматах: JSON, XML и SQLite.

## Содержание

- [Обзор](#обзор)
- [Структура проекта](#структура-проекта)
- [Запуск](#запуск)
- [Сущности предметной области](#сущности-предметной-области)
- [Связи между сущностями](#связи-между-сущностями)
- [Форматы хранения данных](#форматы-хранения-данных)
- [Схема базы данных](#схема-базы-данных)
- [Архитектура кода](#архитектура-кода)
- [Диаграммы](#диаграммы)

## Обзор

Туристическая фирма продаёт путёвки клиентам. Каждая путёвка связана с
одним или несколькими клиентами, одним или несколькими маршрутами, а также
с авиаперевозчиком, туроператором и менеджером, оформившим продажу. Для
каждой путёвки фиксируется платёж с указанием суммы, способа и статуса.

## Структура проекта

```
travel/
├── domain/                       # модель предметной области
│   ├── entity.py                 # базовый класс с уникальным кодом
│   ├── named_entity.py           # сущность с атрибутом name
│   ├── entity_list.py            # базовая коллекция сущностей
│   ├── utils.py                  # общие утилиты (напр. to_int)
│   ├── client.py / client_list.py
│   ├── route.py  / route_list.py
│   ├── package.py / travel_list.py       # путёвка
│   ├── airline.py / airline_list.py
│   ├── tour_operator.py / tour_operator_list.py
│   ├── manager.py / manager_list.py
│   ├── payment.py / payment_list.py
│   ├── package_ext.py / travel_list_ext.py  # путёвка с FK
│   ├── travel_company.py         # базовый агрегатор
│   └── travel_company_ext.py     # агрегатор с расширениями
│
├── dataaccess/                   # сериализация модели
│   ├── data.py                   # абстрактный базовый класс
│   ├── data_json.py / data_json_ext.py   # JSON
│   ├── data_xml.py  / data_xml_ext.py    # XML
│   └── data_sql.py  / data_sql_ext.py    # SQLite
│
├── web/                          # веб-интерфейс на CherryPy
│   ├── layout.py                 # общий HTML-шаблон, экранирование, бейджи
│   ├── clientpage.py             # CRUD клиентов
│   ├── routepage.py              # CRUD маршрутов
│   ├── travelpage.py             # CRUD путёвок (с FK на 4 сущности)
│   ├── airlinepage.py            # CRUD авиаперевозчиков
│   ├── touroperatorpage.py       # CRUD туроператоров
│   ├── managerpage.py            # CRUD менеджеров
│   └── paymentpage.py            # CRUD платежей
│
├── data/
│   └── demo.json                 # демо-данные для запуска
│
├── docs/
│   └── diagrams/                 # UML и ER диаграммы (.mmd, .dot, .png)
│
├── start.py                      # точка входа
└── README.md
```

## Запуск

### Требования

- Python 3.8+
- Пакет CherryPy

```bash
pip install cherrypy
```

### Запуск сервера

```bash
python3 start.py
```

Сервер слушает `http://127.0.0.1:8080`. На главной странице выберите
файл данных (по умолчанию `data/demo.json`) и формат — JSON, XML или
SQL — и нажмите **Открыть**. После загрузки появится главное меню со
ссылками на CRUD-страницы для каждой из семи сущностей.

### Сценарий первого запуска

1. Открыть `data/demo.json` → загрузятся 5 клиентов, 5 маршрутов,
   4 авиаперевозчика, 4 туроператора, 3 менеджера, 5 путёвок и 4 платежа.
2. Перейти на вкладку **Путёвки** — увидите таблицу со всеми связями
   (включая ссылки на платежи и предложение создать платёж для путёвок,
   у которых его ещё нет).
3. Зайти на любую путёвку и изменить состав клиентов / маршрутов / FK.
4. Сохранить как XML или SQL — данные перельются в выбранный формат.
5. Открыть сохранённый файл — все связи (включая FK и платежи) восстановятся.

## Сущности предметной области

| Сущность | Поля |
|---|---|
| **Клиент** (`client`) | code, surname, name, secname, address, phone |
| **Маршрут** (`route`) | code, name, climate, duration, hotel, cost |
| **Путёвка** (`package`) | code, date, quantity, discount + связи |
| **Авиаперевозчик** (`airline`) | code, name, flight_cost |
| **Туроператор** (`touroperator`) | code, name, address, phone, website |
| **Менеджер** (`manager`) | code, surname, name, secname, position, phone, email |
| **Платёж** (`payment`) | code, package_code, date, amount, method, status |

## Связи между сущностями

| От | К | Кратность | Реализация |
|---|---|---|---|
| Путёвка | Клиент | M : N | таблица-связка `package_client` |
| Путёвка | Маршрут | M : N | таблица-связка `package_route` |
| Путёвка | Авиаперевозчик | N : 1 | FK `package.airline_code` |
| Путёвка | Туроператор | N : 1 | FK `package.touroperator_code` |
| Путёвка | Менеджер | N : 1 | FK `package.manager_code` |
| Путёвка | Платёж | 1 : 1 | FK `payment.package_code` UNIQUE |

При удалении сущности связанные записи обновляются:

- удаление **клиента / маршрута** → исключается из всех путёвок;
- удаление **путёвки** → каскадно удаляется её платёж;
- удаление **авиаперевозчика / туроператора / менеджера** → у путёвок
  обнуляется соответствующий FK.

## Форматы хранения данных

Сериализация — единственное, что отличает форматы; модель в памяти
одинакова. Файлы взаимозаменяемы: можно открыть JSON и сохранить как SQL,
открыть SQL и сохранить как XML, и т.д. Round-trip сохраняет все связи.

### JSON
Один объект верхнего уровня с массивами по каждой сущности. Связи
M:N представлены массивами кодов внутри `travels[*].clients`/`routes`,
FK — обычными целочисленными полями.

```json
{
  "clients": [{"code": 1, "surname": "Иванов", ...}],
  "travels": [{
    "code": 1, "date": "15.05.2026", "quantity": 2, "discount": 5,
    "clients": [1, 2], "routes": [1],
    "airline_code": 2, "touroperator_code": 1, "manager_code": 1
  }],
  "payments": [{"code": 1, "package_code": 1, "amount": 180500, ...}]
}
```

### XML
Структурно эквивалентен JSON: корень `<travelcompany>`, дочерние элементы —
коллекции, внутри них элементы конкретных сущностей. M:N представлены
вложенными элементами `<clients><client code="1"/></clients>`.

### SQLite
9 таблиц: 7 для сущностей + 2 связки (`package_client`, `package_route`).
Все запросы параметризованные. Все FK имеют ON DELETE/UPDATE CASCADE.
При каждом открытии соединения выполняется `PRAGMA foreign_keys = ON`, иначе
в SQLite ограничения FK по умолчанию не проверяются.

## Схема базы данных

```
client(code, surname, name, secname, address, phone)
routes(code, name, climate, duration, hotel, cost)
package(code, date, quantity, discount,
        airline_code, touroperator_code, manager_code)
package_client(code, package, client)        UNIQUE(package, client)
package_route(code, package, routes)         UNIQUE(package, routes)
airline(code, name, flight_cost)
touroperator(code, name, address, phone, website)
manager(code, surname, name, secname, position, phone, email)
payment(code, package_code UNIQUE, date, amount, method, status)
```

Все FK — `ON UPDATE CASCADE ON DELETE CASCADE`. UNIQUE на `payment.package_code`
обеспечивает связь 1:1 между путёвкой и платежом на уровне БД.

## Архитектура кода

Модель построена по принципу разделения ответственностей:

- **`domain/`** — пассивные доменные объекты и коллекции, не знают
  ничего о форматах хранения и интерфейсе. `entity` → `named_entity` →
  конкретные сущности; параллельная иерархия для коллекций
  `entity_list` → специализированные списки.

- **`dataaccess/`** — сериализаторы. Базовая реализация работает с тремя
  ключевыми сущностями (`client`, `route`, `package`). Расширения
  (`*_ext`) добавляют поддержку четырёх дополнительных сущностей и FK
  через наследование, переопределяя методы `read()`, `write()`,
  `read_package_table()` / `write_package_table()` и т.п.

- **`web/`** — CherryPy-страницы с CRUD-операциями. Каждая страница
  принимает экземпляр библиотеки `TravelCompanyExt` и работает с ней
  напрямую без промежуточного слоя сервисов. Общий шаблон, экранирование
  и стилизация вынесены в `web/layout.py`.

Расширение модели новыми сущностями (например, добавить «Поставщика
страховки») потребует:

1. Создать классы `insurer` и `insurerList` в `domain/`.
2. Добавить FK `insurer_code` в `package_ext`.
3. Добавить методы `create_insurer` / … в `TravelCompanyExt`.
4. Дополнить три сериализатора (`*_ext`) чтением/записью новой таблицы.
5. Создать `web/insurerpage.py` и зарегистрировать в `start.py`.

Базовые классы (`package`, `TravelCompany`, базовые сериализаторы и т.д.)
остаются нетронутыми.

## Диаграммы

В каталоге `docs/diagrams/`:

| Файл | Описание |
|---|---|
| `class_entities.{mmd,dot,png}` | Иерархия сущностей и связи M:N |
| `class_storage.{mmd,dot,png}` | Коллекции и агрегатор `TravelCompany` |
| `er_diagram.{mmd,dot,png}` | ER-схема БД SQLite |

Исходники в формате [Mermaid](https://mermaid.js.org) (`.mmd`) можно
открыть на [mermaid.live](https://mermaid.live), исходники Graphviz
(`.dot`) — рендерить командой `dot -Tpng file.dot -o file.png`.
