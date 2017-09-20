# -*- coding: utf-8 -*-
import ast
from bs4 import BeautifulSoup
from collections import defaultdict
try:
    # project_path = path.dirname( path.dirname( path.abspath(__file__) ) )
    # app_root = path.dirname( path.abspath(__file__) )
    #
    # print(f"project_path: {project_path}")
    # print(f"app_root: {app_root}")
    # sys.path.append(app_root)
    from DateTimeProcess import datetime_process
except:
    from .DateTimeProcess import datetime_process
import grequests
#from event_placement.celery import app
from celery import Task
from gevent import monkey
import socket
from importlib import reload
import sys
from os import path
import json
import re
path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path)
reload(socket)
import requests

def make_dict():
    return defaultdict(make_dict)


@staticmethod
def exception(self, request, exception):
    print("Problem: {url}: {exception}".format(
        url=request.url,
        exception=exception))


class Spiders:

    def __init__(self):
        self.d = defaultdict(make_dict)
        self.url = "http://caribbean.com.ua/{lang}/?s=&cat=73%2C67&start_day=now"
        self.lang_regex = r'(?<=/)[a-z]{2}(?=/)'
        self.code_regex = r'\{[\w\W]*}'
        self.LANG_LIST = ('ua', 'ru', 'en')
        self.urls = []
        # self.results = []
        # self.fields = {}
        # self.fields = {}
        # self.p_name = None
        # self.lang = None
        # self.soup_select = None
        # self.link_select = None
        # self.results = None
        # self.import_ = None
        # self.p_name = None
        # self.soup_select = None
        # self.link_select = None
        # self.out_path = None

        [self.urls.append(self.url.format(lang=lang))
            for lang in self.LANG_LIST]

        #self.url = url
        if 'caribbean.com.ua' in self.url:
            self.p_name = 'CA'
            self.soup_select = 'div.col-sm-4'
            self.link_select = 'div.b-title > a'
            self.fields = {
                'name': 'div.b-title > a',
                'month': 'div.b-monthe',
                'day': 'div.b-day',
                'time_start': 'div.b-start-day > span',
                'price': 'div.b-tiket > span',
            }

    def start_parse(self):

        self.out_path = 'spiders/data/%s_events.txt' % self.p_name

        if 'caribbean.com.ua' in self.url:
            #print(self.parse_caribbean())
            return self.parse_caribbean()


    def parse_caribbean(self):

        monkey.patch_socket()
        #try:
        self.results = grequests.map((grequests.get(u) for u in self.urls),
                                     exception_handler=exception,
                                     size=3)
        #print(f"self.results @method_async_decorator: {self.results}")
        #print("MAKE FINALLY-----")
        # grequests has done its job
        reload(socket)

        #print(f"!!!results: {self.results}")
        #print ("Class @parse_caribbean(self.urls): %s" % (self.urls))

        for result in self.results:
            soup = BeautifulSoup(result.text, 'lxml')
            # print(len(soup))

            for i, event_ in enumerate(soup.select(self.soup_select)):
                link = event_.select(self.link_select)[0].get('href')
                cur_language = re.search(self.lang_regex, link).group()

                self.d[cur_language][i]['link'] = link

                for key, val in self.fields.items():
                    try:
                        self.d[cur_language][i][key] = (
                        event_.select(val)[0].get_text().strip()
                        )
                    except KeyError:
                        pass

                    if key in max(self.fields.keys()):
                        self.d[cur_language][i] = datetime_process(
                        dict(self.d[cur_language][i]))


        #print("Class @save_result_to_file(out_path): %s" % (self.out_path))
        with open(self.out_path, 'w', encoding='utf-8') as file:
            file.write(f"{json.loads(json.dumps(self.d))}")
            return self.out_path


#         wfile_path = os.path.join(app_root, self.out_path).replace(r'\\', '/')
#         with open(file_path, 'w', encoding='utf-8') as file:
#             file.write(f"{json.loads(json.dumps(self.d))}")

    # def file_to_db(self):
    #     self.import_ = ImportDb(self.out_path)
    #     return self.import_.import_to_db()

class Parter:
    url_get = 'http://parter.ua/en/event/concert-hall/caribbean_club.html'
    p_name = 'PA'
    out_path = 'spiders/data/%s_events.txt' % p_name
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
            return self.out_path



class Karabas:
    cut_time_regex = r':00\+\d{2}:00|T'
    lang_regex = r'(?<=/)[a-z]{2}(?=/)'
    code_regex = r'\{[\w\W]*}'
    dd = defaultdict(make_dict)
    LANG_LIST = ('ua', 'ru', 'en')
    urls = []

    for lang in LANG_LIST:
        urls.append('https://karabas.com/{}/caribbean-club/'.format(lang))

    p_name = 'KA'
    out_path = 'spiders/data/%s_events.txt' % p_name


    def exception(self, request, exception):
        print("Problem: {}: {}".format(request.url, exception))

    def async(self):
        monkey.patch_socket()

        results = grequests.map((grequests.get(u) for u in self.urls),
                                 exception_handler=self.exception,
                                 size=3)
        # grequests has done its job
        reload(socket)
        return self.parse(results)

    def parse(self, results):
        for result in results:
            soup = BeautifulSoup(result.text, 'lxml')

            event_obj_list = soup.select("div.block-mini > script")
            for i, event_ in enumerate(event_obj_list):
                get_code = re.search(self.code_regex, str(event_)).group()

                d = ast.literal_eval('%s' % get_code)
                link = d['offers']['url']

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

        with open(self.out_path, 'w') as file:
            json.dump(self.dd, file)
            return self.out_path


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
    out_path = 'spiders/data/%s_events.txt' % p_name
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
                    self.dd['%s' % self.lang]['%d' % i][val] = (
                        re.sub(
                                self.cut_time_regex, ' ', d[key]
                                ).strip()
                    )
                else:
                    self.dd['%s' % self.lang]['%d' % i][val] = d[key]

        with open(self.out_path, 'w') as file:
            json.dump(self.dd, file)
            return self.out_path

if __name__ == "__main__":
    url = "http://caribbean.com.ua/{lang}/?s=&cat=73%2C67&start_day=now"
    l_ = Spiders()
    #print(l.__dict__)
    l_.start_parse()
    # выведет: Мне 26, а ты бы сколько дал?
