import ast
import html
import os
import re
import sys

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'event_placement.settings.base'
import django
django.setup()
from events.models import Event, Platform


class ImportDb:

    def __init__(self, path):

        # timezone.activate(pytz.timezone("Europe/Kiev"))
        self.path = path
        # print(path)

        self.PLATFORM_NAMES = {
                'CA': 'Caribbean Club',
                'KA': 'Karabas.com',
                'CO': 'Concert.ua',
                'PA': "Parter.ua"
        }

    def import_to_db(self):
        place_code = re.search(r'[^\/|\\]+(?=_events)', self.path).group()
        platform_name = self.PLATFORM_NAMES[place_code]
        print(platform_name)
        # pass

        with open(self.path, encoding="utf-8", newline='') as dictfile:
            ev_dict = ast.literal_eval(dictfile.read())

        for lang, value in ev_dict.items():
            # i = 0
            for ev_value in value.values():
                # print(ev_value['link'])
                # print(ev_value['name'])
                # print(ev_value['date'])

                event = Event()


                event.platform = Platform.objects.get(
                        name=platform_name
                )
                event.name = html.unescape(ev_value['name'])
                event.link = ev_value['link']
                event.date = ev_value['date']
                event.language = lang
                try:
                    event.save()
                except Exception as e:
                    print(e)
