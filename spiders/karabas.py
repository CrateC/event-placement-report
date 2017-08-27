import ast
import json
import re
from collections import defaultdict

import grequests
from bs4 import BeautifulSoup
from import_db import ImportDb


def make_dict():
    return defaultdict(make_dict)

class Karabas:
    cut_time_regex = r':00\+\d{2}:00|T'
    lang_regex = r'(?<=/)[a-z]{2}(?=/)'
    code_regex = r'\{[\w\W]*}'
    dd = defaultdict(make_dict)
    LANG_LIST = ('ua', 'ru', 'en')
    urls = []

    for lang in LANG_LIST:
        urls.append(f'https://karabas.com/{lang}/caribbean-club/')


    p_name = 'KA'
    out_path = f'data/{p_name}_events.txt'



    def exception(self, request, exception):
        print("Problem: {}: {}".format(request.url, exception))

    def async(self):
        results = grequests.map((grequests.get(u) for u in self.urls),
                                 exception_handler=self.exception,
                                 size=3)

        return self.parse(results)

    def parse(self, results):
        for result in results:
            # print(result.text)
            soup = BeautifulSoup(result.text, 'lxml')

            # dd = {}
            event_obj_list = soup.select("div.block-mini > script")
            for i, event_ in enumerate(event_obj_list):
                get_code = re.search(self.code_regex, str(event_)).group()

                d = ast.literal_eval(f'{get_code}')
                link = d['offers']['url']

                #print(link)
                try:
                    cur_leng = re.search(self.lang_regex, link).group()
                except:
                    cur_leng = 'ru'

                self.dd[cur_leng][i]['link'] = (
                    d['offers']['url'].replace('order/', '')
                )
                self.dd[cur_leng][i]['name'] = d['name']
                self.dd[cur_leng][i]['date'] = re.sub(
                    self.cut_time_regex, ' ', d['startDate']
                ).strip()

                # dd[cur_leng][i] =  d['name'], \
                #                         d['offers']['url'],\
                #                         d['offers']['offerCount'],\
                #                         d['startDate']

        with open(self.out_path, 'w') as file:
            json.dump(self.dd, file)

        # Importing to Database

        import_ = ImportDb(self.out_path)
        import_.import_to_db()

karabas = Karabas()
karabas.async()
