import ast
import json
import re
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from import_db import ImportDb


def make_dict():
    return defaultdict(make_dict)
import sys
sys.setdefaultencoding(‘utf-8’)

class Concert:
    cut_time_regex = ':00\+\d{2}:00|T'
    dd = defaultdict(make_dict)
    url_get = 'https://www.concert.ua/kiev/caribbean-club'
    headers_get = {
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'https://www.concert.ua/',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.8',
            }

    p_name = 'CO'
    out_path = f'data/{p_name}_events.txt'
    lang = 'ru'

    fields = {
        'url': 'link',
        'name': 'name',
        'startDate': 'date'
        }

    def not_async(self):
        # r = requests.get(self.url_get, headers=self.headers_get)
        return self.parse(
                            requests.get(
                                self.url_get,
                                headers=self.headers_get
                            ).text
        )

    def parse(self, response):
        soup = BeautifulSoup(response, 'lxml')
        event_obj_list = soup.select("div.container > script")

        for i, event_ in enumerate(event_obj_list):
            get_code = re.search(
                                 '\{[\w\W]*}', str(event_)
                                 ).group()
            d = ast.literal_eval(get_code)


            for key, val in self.fields.items():

                if val is 'date':
                    self.dd[f'{self.lang}'][f'{i}'][val] = (
                        re.sub(
                                self.cut_time_regex, ' ', d[key]
                                ).strip()
                    )
                else:
                    self.dd[f'{self.lang}'][f'{i}'][val] = d[key]

        with open(self.out_path, 'w') as file:
            json.dump(self.dd, file)

        # From File to Database
        import_ = ImportDb(self.out_path)
        import_.import_to_db()

concert = Concert()
concert.not_async()
