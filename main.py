from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

WINERY_FOUNDATION_YEAR = 1920
BEVERAGES_DATA_FILE = r'data/wine.xlsx'

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

winery_age = datetime.now().year - WINERY_FOUNDATION_YEAR

beverages_df = pd.read_excel(
    io=BEVERAGES_DATA_FILE,
    sheet_name='Лист1',
    na_values="nan",
    keep_default_na=False,
).sort_values(by='Категория')

beverages = beverages_df.to_dict(orient='records')

beverages_categories = defaultdict(list)
for beverage in beverages:
    beverages_categories[beverage['Категория']].append(beverage)

rendered_page = template.render(
    winery_age=winery_age,
    beverages_categories=beverages_categories,
)

with open('index.html', 'w') as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
