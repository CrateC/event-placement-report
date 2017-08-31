import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.views.generic import ListView
from utils.query_to_dict import convert_query_to_dict, convert_sqlite_query_to_dict

from .models import Event
from django.db import connection


class EventsPlacementListView(LoginRequiredMixin, ListView):

    # login_url = '/au/login/'
    template_name = 'events/export.html'
    db_name = connection.settings_dict['NAME']

    @staticmethod
    def count_events(pl_id_):

        return Event.objects.filter(
                            platform='{}'.format(pl_id_),
                            date__gte=datetime.datetime.now(),
                            language='ru'
                ).order_by('date').count()

    # @staff_member_required
    def get_queryset(self):

        cursor = connection.cursor()
        columns = ['date', 'name']
        tbl_names = ['ca', 'pa', 'ka', 'co']
        dc = {}

        if connection.vendor == 'sqlite3':
            for tbl_name_ in tbl_names:

                cursor.execute(
                    """
                        SELECT id FROM events_platforms
                        WHERE short_name='{}';
                    """.format(tbl_name_.upper())
                )
                pl_id = cursor.fetchone()[0]

                if tbl_name_.upper() in ['CA', 'CO', 'KA', 'PA']:
                    dc["{}".format(tbl_name_.upper())] = self.count_events(pl_id)

                cursor.execute(
                    """
                        DROP TABLE IF EXISTS {}
                    """.format(tbl_name_.upper()))

                cursor.execute(
                    """
                        CREATE TEMP TABLE IF NOT EXISTS {} AS SELECT name,(link) as {}, date
                        FROM {events_events}
                        WHERE platform_id = (SELECT id FROM events_platforms
                        WHERE short_name='{}') AND language = 'ru'
                                            GROUP BY date order by date
                    """.format(
                        tbl_name_.upper(),
                        tbl_name_.upper(),
                        tbl_name_.upper())
                    )

                columns.append(tbl_name_.upper())

            cursor.execute(
                """
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

            return convert_sqlite_query_to_dict("""%s""" % events_data)

        elif connection.vendor == 'mysql':
            for tbl_name_ in tbl_names:

                cursor.execute(
                    """
                        SELECT id FROM events_platforms
                        WHERE short_name='{}';
                    """.format(tbl_name_.upper())
                )
                pl_id = cursor.fetchone()[0]
                #print(f"---------PL_ID: {pl_id}")

                if tbl_name_.upper() in ['CA', 'CO', 'KA', 'PA']:
                    dc["{}".format(tbl_name_.upper())] = self.count_events(pl_id)

                cursor.execute(
                    """
                        DROP TABLE IF EXISTS {}
                    """.format(tbl_name_.upper()))

                cursor.execute(
                    """
                        CREATE TEMPORARY TABLE IF NOT EXISTS {0} AS (
                            SELECT name,(link) as {0}, date
                            FROM events_events
                            WHERE platform_id = (SELECT id FROM events_platforms
                        WHERE short_name='{0}') AND language = 'ru'
                        GROUP BY date ORDER BY date
                        );
                    """.format(
                        tbl_name_.upper(),
                    )
                )

                columns.append(tbl_name_.upper())

            cursor.execute(
                """
                    SELECT
                    t1.date,t1.name,t1.CA,
                    t2.PA,
                    t4.CO,
                    t3.KA

                    FROM CA AS t1

                        LEFT JOIN PA AS t2 ON t1.date = t2.date

                        LEFT JOIN KA AS t3 ON t1.date = t3.date

                        LEFT JOIN CO AS t4 ON t1.date = t4.date

                    WHERE t1.date > CURDATE()
                    ORDER BY date
                """)

            events_data = cursor.fetchall()
            print(type(events_data))
            cursor.close()
            return convert_query_to_dict("""{}""".format(events_data,))
