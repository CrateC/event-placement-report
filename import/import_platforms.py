import csv
import os
import sys

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'event_placement.settings.base'
import django
django.setup()

from events.models import Platform

import_path = r'platform.txt'

# PLATFORM_NAMES = {
#         'CA': 'Caribbean Club',
#         'KA': 'Karabas.com',
#         'CO': 'Concert.ua',
# }

PL_NAMES = {
        'Caribbean Club': 'CA',
        'Karabas.com'   : 'KA',
        'Concert.ua'    : 'CO',
        'Parter.ua'     : 'PA',
}

with open(import_path, encoding="utf-8", newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=',')

    for row in data:
        if row[1] != 'link':

            pl = Platform()

            pl.name = row[0]
            pl.short_name = PL_NAMES[row[0]]
            pl.link = row[1]
            pl.category = row[2]
            try:
                pl.save()
            except:
                pass
