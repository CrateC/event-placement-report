# -*- coding: utf-8 -*-
import configparser
# from gevent import monkey; monkey.patch_all(thread=False)
import gevent.monkey
gevent.monkey.patch_ssl()#(thread=False)
import requests
import pendulum
import json
import time
import datetime
import os
import sys


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'event_placement.settings.production'


class Facebook:

    def __init__(self, p_name):

        import django
        django.setup()
        from events.models import Event, Platform

        self.p_name = p_name
        self.page = Platform.objects.filter(short_name=self.p_name).values()[0]['link']

        print()
        print(self.page)
        print()

    def get_event_data(self):
        config = configparser.RawConfigParser()
        config.read('spiders/spisers.config.cfg')
        # print(config.sections())

        base = config['FB']['base']
        fields = config['FB']['fields']
        limit = '&limit=%s' % config['FB']['limit']
        parameters = '&access_token=%s' % config['FB']['access_token']
        page_link = self.page

        url = base + self.page + fields + limit + parameters

        print()
        print(url)
        print()

        return url

    def request_until_succeed(self):
        url = self.get_event_data()
        req = requests.get(url)

        success = False

        while success is False:
            try:
                if req.status_code == 200:
                    success = True
            except Exception as e:
                print(e)
                time.sleep(5)
                print(
                    "Error for URL %s: %s" % (
                        url,
                        datetime.datetime.now())
                    )
        return req.text



    def process_dict(self):
        lang = 'ru'
        base_url = 'https://www.facebook.com/events/'

        j = json.loads(self.request_until_succeed())

        dd = {}
        dd[lang] = {}
        for i, list_item in enumerate(j['data']):
            for k, val in list_item.items():
                dd[lang][f"{i}"] = {}
                dd[lang][f"{i}"]['name'] = list_item['name']
                dd[lang][f"{i}"]['link'] = f"{base_url}{list_item['id']}"
                dd[lang][f"{i}"]['date'] = dt_conert(list_item['start_time'])
            #     break
            # break
        print(dd)

        out_path = 'spiders/data/fb_%s_events.txt' % self.p_name
        with open(out_path, 'w') as outfile:
            outfile.writelines(str(dd))
            return out_path

def dt_conert(dt):
    return pendulum.parse(dt, strict=True).format('%Y-%m-%d %H:%M')

if __name__ == "__main__":
    p_name = 'FC'
    fb = Facebook(p_name)
    #j = json.loads(fb.request_until_succeed())
    path = fb.process_dict()
    print(path)
    #return path
