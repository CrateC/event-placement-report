import requests
from DateTimeProcess import datetime_process
from bs4 import BeautifulSoup
from import_db import ImportDb

class Parter:
    url_get = 'http://parter.ua/en/event/concert-hall/caribbean_club.html'
    p_name = 'PA'
    out_path = 'data/%s_events.txt' % p_name
    lang = 'ru'

    fields = {
            'name': 'a.eventtitle',
            'date': 'tr:nth-of-type(3) > td:nth-of-type(1)',
    }

    def not_async(self):
        return self.parse(
                            requests.get(
                                self.url_get
                            ).text
        )

    def parse(self, response):
        soup = BeautifulSoup(response, 'lxml')
        dd = dict()
        dd['%s' % self.lang] = {}

        for i, event_ in enumerate(soup.select("td.event")):
            dd['%s' % self.lang]['%d' % i] = {}

            link = event_.select(
                "a.eventtitle")[0].get(
                "href").replace(
                "/en/", "/%s/" % self.lang
                )

            dd['%s' % self.lang]['%d' % i]['link'] = (
                'http://parter.ua{}'.format(link)
            )

            for k, v in self.fields.items():
                if k in 'date':
                    data_ = event_.select(v)[0].get_text()
                    dd['%s' % self.lang]['%d' % i][k] = datetime_process(data_)
                else:
                    dd['%s' % self.lang]['%d' % i][k] = event_.select(v)[0].get_text()

        with open(self.out_path, 'w', encoding='utf-8') as file:
            file.write(str(dd))

        import_ = ImportDb(self.out_path)
        import_.import_to_db()
