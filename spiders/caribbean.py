import json
import re
from collections import defaultdict

import grequests
from DateTimeProcess import datetime_process
from bs4 import BeautifulSoup
from import_db import ImportDb


def make_dict():
    return defaultdict(make_dict)

class Caribbean:
    dd = defaultdict(make_dict)
    LANG_LIST = ('ua', 'ru', 'en')
    urls = []

    for lang in LANG_LIST:
        urls.append(
            f'http://caribbean.com.ua/{lang}/'
            '?s=&cat=73%2C67&start_day=now'
        )

    p_name = 'CA'
    out_path = f'data/{p_name}_events.txt'

    fields = {
        'name': 'div.b-title > a',
        'month': 'div.b-monthe',
        'day': 'div.b-day',
        'time_start': 'div.b-start-day > span',
        'price': 'div.b-tiket > span',
    }

    @staticmethod
    def exception(request, exception):
        print("Problem: {}: {}".format(request.url, exception))

    def async(self):
        results = grequests.map(
                               (grequests.get(u) for u in self.urls),
                                exception_handler=self.exception,
                                size=3
        )
        return self.parse_posts(results)

    def parse_posts(self, results):
        for result in results:
            soup = BeautifulSoup(result.text, 'lxml')

            for self.i, event_ in enumerate(soup.select("div.col-sm-4")):

                link = event_.select("div.b-title > a")[0].get('href')
                cur_lenght = re.search(r'(?<=/)[a-z]{2}(?=/)', link).group()

                print(f"cur_lenght_0: {cur_lenght}")
                self.dd[cur_lenght][self.i]['link'] = link

                for key, val in self.fields.items():
                    try:
                        self.dd[cur_lenght][self.i][key] = (
                            event_.select(val)[0].get_text().strip()
                        )
                    except:
                        pass

                    if key in max(self.fields.keys()):
                        self.dd[cur_lenght][self.i] = datetime_process(dict(self.dd[cur_lenght][self.i]))

        with open(self.out_path, 'w') as file:
            json.dump(self.dd, file)

        if self.dd:
            # Importing to Database
            import_ = ImportDb(self.out_path)
            import_.import_to_db()


caribbean = Caribbean()
caribbean.async()
