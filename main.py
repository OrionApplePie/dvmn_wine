from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from utils import get_age_declension

WINERY_FOUNDATION_YEAR = 1920
BEVERAGES_FILEPATH = r'data/wine.xlsx'

def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    winery_age = datetime.now().year - WINERY_FOUNDATION_YEAR
    winery_age_phrase = f' {winery_age} {get_age_declension(winery_age)}'

    beverages_df = pd.read_excel(
        io=BEVERAGES_FILEPATH,
        sheet_name='Лист1',
        na_values='nan',
        keep_default_na=False,
    ).sort_values(by='Категория')

    beverages = beverages_df.to_dict(orient='records')

    beverages_by_categories = defaultdict(list)

    for beverage in beverages:
        beverages_by_categories[beverage['Категория']].append(beverage)

    rendered_page = template.render(
        winery_age_phrase=winery_age_phrase,
        beverages_by_categories=beverages_by_categories,
    )

    with open('index.html', 'w') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
