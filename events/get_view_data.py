import datetime
import os
import sys
# from django_mysql.models import QuerySet
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(project_dir)
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'event_placement.settings.production'

import django
django.setup()
#from django.db import connection
#from django.views.generic import ListView
#from django.db import connection
from utils.query_to_dict import convert_qslist_to_dict
from events.models import Event, Platform
from events.queries import SELECT_ID, DROP_TABLE
from events.queries import MYSQL_CREATE_TEMP, MYSQL_LEFT_JOIN
from events.queries import SQLITE3_CREATE_TEMP, SQLITE3_LEFT_JOIN




def get_queryset_data():
    QS_LIST = []
    f = '%Y-%m-%d %H:%M'

    queryset = Platform.objects.values_list('short_name', flat=True)
    tbl_names = [x for x in queryset]

    platform_list = Platform.objects.values('id', 'short_name')
    print(f"platform_list: {platform_list}")
    print(len(platform_list))

    for platform in platform_list:
        qss = Event.objects.values(
                'date',
                'name',
                'link'
            ).distinct().filter(
                platform_id=platform['id'],
                date__gte=datetime.datetime.now(),
                language='ru'
            ).order_by('date').sql_small_result()

        QS_LIST.append(qss)

    # ll = QS_LIST[0] | QS_LIST[1] | QS_LIST[2] | QS_LIST[3]

    cll = []
    for ca in QS_LIST[0]:
        cl = ca['date'].strftime(f), ca['name'], ca['link']
        tcl = ()

        for qi in range(1, len(platform_list)):
            for qli, pa in enumerate(QS_LIST[qi]):
                if pa['date'] == ca['date']:
                    tcl += pa['link'],
                    break
                else:
                    if qli == len(QS_LIST[qi])-1:
                        tcl += ('None',)
                        break
        cll.append(cl + tcl)
    print(cll)
    return cll


if __name__ == "__main__":
    get_queryset_data()
