"""Простые HTML-обёртки для CherryPy-страниц (без шаблонизатора, для простоты)."""

import html


def esc(value):
    """Экранирование HTML для безопасной вставки в страницу."""
    if value is None:
        return ''
    return html.escape(str(value), quote=True)


def page(title, body, breadcrumbs=''):
    """Минимальный HTML-каркас с CSS, общим для всех страниц."""
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>{esc(title)} — Турфирма</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif;
          margin: 20px; color: #222; }}
  h1 {{ margin: 0 0 12px; font-size: 22px; }}
  table {{ border-collapse: collapse; margin-top: 10px; }}
  th, td {{ padding: 6px 10px; border: 1px solid #bbb; vertical-align: top; }}
  th {{ background: #444; color: #fff; text-align: left; }}
  tr:nth-child(even) td {{ background: #f4f4f4; }}
  a {{ color: #0a58ca; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .nav {{ margin-bottom: 16px; padding: 8px 0; border-bottom: 1px solid #ddd; }}
  .nav a {{ margin-right: 14px; }}
  .crumbs {{ color: #888; font-size: 13px; margin-bottom: 10px; }}
  form table td {{ border: none; padding: 4px 6px; }}
  input[type=text], input[type=number], input[type=email],
  select, textarea {{ padding: 4px 6px; min-width: 200px;
                      border: 1px solid #aaa; border-radius: 3px; }}
  input[type=submit], button {{
      padding: 6px 14px; background: #0a58ca; color: white;
      border: 0; border-radius: 3px; cursor: pointer; }}
  input[type=submit]:hover {{ background: #0746a0; }}
  .badge {{ display: inline-block; padding: 1px 6px; border-radius: 3px;
            font-size: 12px; color: white; }}
  .badge-paid {{ background: #28a745; }}
  .badge-wait {{ background: #f0ad4e; }}
  .badge-cancel {{ background: #888; }}
  .muted {{ color: #888; }}
</style>
</head>
<body>
<div class="nav">
  <a href="/">Главная</a>
  <a href="/clientpage/">Клиенты</a>
  <a href="/routepage/">Маршруты</a>
  <a href="/travelpage/">Путёвки</a>
  <a href="/airlinepage/">Авиаперевозчики</a>
  <a href="/touroperatorpage/">Туроператоры</a>
  <a href="/managerpage/">Менеджеры</a>
  <a href="/paymentpage/">Платежи</a>
</div>
<div class="crumbs">{breadcrumbs}</div>
<h1>{esc(title)}</h1>
{body}
</body>
</html>'''


def status_badge(status):
    """Текстовый статус платежа без цветного оформления."""
    return esc(status)


def back_link(href='index', text='назад'):
    return f'<p><a href="{href}">← {esc(text)}</a></p>'
