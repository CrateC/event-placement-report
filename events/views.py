import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.views.generic import ListView
from utils.query_to_dict import convert_query_to_dict, convert_sqlite_query_to_dict

from .models import Event


class EventsPlacementListView(LoginRequiredMixin, ListView):

    # login_url = '/au/login/'
    template_name = 'events/export.html'

    @staticmethod
    def count_events(pl_id_):

        return Event.objects.filter(
                            platform=f'{pl_id_}',
                            date__gte=datetime.datetime.now(),
                            language='ru'
                ).order_by('date').count()

    # @staff_member_required
    def get_queryset(self):

        cursor = connection.cursor()
        columns = ['date', 'name']
        tbl_names = ['ca', 'pa', 'ka', 'co']
        dc = {}

        for tbl_name_ in tbl_names:
            cursor.execute(
                f"""
                    SELECT id FROM events_platforms
                    WHERE short_name='{tbl_name_.upper()}';
            """)
            pl_id = cursor.fetchone()[0]

            if f'{tbl_name_.upper()}' in ['CA', 'CO', 'KA', 'PA']:
                dc[f"{tbl_name_.upper()}"] = self.count_events(pl_id)

            cursor.execute(
                f"""
                    DROP TABLE IF EXISTS {tbl_name_.upper()}
            """)
            cursor.execute(
                f"""

                    CREATE TEMP TABLE IF NOT EXISTS {tbl_name_.upper()} AS SELECT name,(link) as {tbl_name_.upper()}, date
                    FROM events_events
                    WHERE platform_id = (SELECT id FROM events_platforms
                    WHERE short_name='{tbl_name_.upper()}') AND language = 'ru'
                                        GROUP BY date order by date
            """)
            columns.append(f'{tbl_name_.upper()}')

        cursor.execute(
        f"""
            SELECT
            t1.date, t1.name, t1.CA,
            t2.PA,
            t4.CO,
            t3.KA

            FROM temp.CA AS t1

            LEFT JOIN temp.PA AS t2 ON t1.date = t2.date

            LEFT JOIN temp.KA AS t3 ON t1.date = t3.date

            LEFT JOIN temp.CO AS t4 ON t1.date = t4.date

            WHERE t1.date > datetime('NOW')
            ORDER BY t1.date;
        """)

        events_data = cursor.fetchall()
        cursor.close()
        # print(events_data)
        return convert_sqlite_query_to_dict(f"""{events_data}""")
        # return convert_query_to_dict(f"""{events_data}""")
