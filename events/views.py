import datetime
from django_mysql.models import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.views.generic import ListView
# from django.db.models import CharField, Case, Value, When, F, Q, IntegerField
try:
    from utils.query_to_dict import convert_query_to_dict, convert_qslist_to_dict
except:
    from utils.query_to_dict import convert_sqlite_query_to_dict
from .get_view_data import get_queryset_data
from .tasks import get_query
from .models import Event, Platform
from django.http import HttpResponse
from .queries import SELECT_ID, DROP_TABLE
from .queries import MYSQL_CREATE_TEMP, MYSQL_LEFT_JOIN
from .queries import SQLITE3_CREATE_TEMP, SQLITE3_LEFT_JOIN


from django.shortcuts import render
from celery.result import AsyncResult
from django.core.cache import cache


class EventsPlacemenOrmView(LoginRequiredMixin, ListView):
    template_name = 'events/export.html'

    def get_queryset(self):

        cache_key = 'Nlfjhdfyy!&pYEFmkFZN13451' # needs to be unique
        cache_time = 86400 # time in seconds for cache to be valid
        task_result = cache.get('task_result')
        if not task_result:
            task_result = get_query.delay().get()
            cache.set(cache_key, task_result, cache_time)
            # cache.set(
            #         'task_result',
            #         task_result,
            #         depends_on=[Event]
            # )
        return (task_result)


    # def get_queryset(self):
    #     task_result = cache.get('task_result')
    #     if not task_result:
    #         task_result = get_query.delay().get()
    #         cache.set(
    #                 'task_result',
    #                 task_result,
    #                 depends_on=[Event]
    #         )
    #     return task_result
        # task_result = get_query.delay().get()
        #
        # # if you need to use the task_id somewhere else
        # # async_result = AsyncResult(id=task_result.id)
        # return task_result


class EventsPlacementListView(LoginRequiredMixin, ListView):

    # login_url = '/au/login/'
    template_name = 'events/export.html'
    db_name = connection.settings_dict['NAME']
    tbl_names = ['CA', 'PA', 'CO', 'KA']
    #['ca', 'pa', 'ka', 'co']

    @staticmethod
    def count_events(pl_id_):

        return Event.objects.filter(
                            platform='{}'.format(pl_id_),
                            date__gte=datetime.datetime.now(),
                            language='ru'
                ).order_by('date').count()

    # @staff_member_required
    def get_queryset(self):
        """ SELECT_ID, DROP_TABLE
        """
        cursor = connection.cursor()
        columns = ['date', 'name']
        dc = {}

        for i, tbl_name in enumerate(self.tbl_names):
            # print("")
            # print("")
            # print(f"tbl_name: {tbl_name}")
            # print("")
            # print("")
            # print(f"SELECT_ID: {SELECT_ID.format(tbl_name)}")
            # print("")
            cursor.execute(SELECT_ID.format(tbl_name))
            pl_id = cursor.fetchone()[0]

            if tbl_name in self.tbl_names:
                dc["{}".format(tbl_name)] = self.count_events(pl_id)

            cursor.execute(DROP_TABLE.format(tbl_name))
            #print(DROP_TABLE.format(tbl_name))

            if connection.vendor == 'mysql':
                """ MYSQL_CREATE_TEMP, MYSQL_LEFT_JOIN
                """

                # print(f"{MYSQL_CREATE_TEMP.format(tbl_name)}")
                cursor.execute(f"{MYSQL_CREATE_TEMP.format(tbl_name)}")
                columns.append(tbl_name)

                if i == len(self.tbl_names)-1:
                    # print(f"dc : {dc}")
                    # print(f"MYSQL_LEFT_JOIN: {MYSQL_LEFT_JOIN}")
                    cursor.execute(MYSQL_LEFT_JOIN)
                    events_data = cursor.fetchall()
                    # print(type(events_data))
                    cursor.close()
                    #return convert_query_to_dict("""{}""".format(events_data,))


            elif connection.vendor == 'sqlite3':
                """ SQLITE3_CREATE_TEMP, SQLITE3_LEFT_JOIN
                """
                #for tbl_name in self.tbl_names:

                cursor.execute(SQLITE3_CREATE_TEMP.format(tbl_name))
                columns.append(tbl_name)
                #continue

                if tbl_name in max(self.tbl_names):
                    cursor.execute(SQLITE3_LEFT_JOIN)
                    events_data = cursor.fetchall()
                    cursor.close()
                    #return convert_sqlite_query_to_dict("""%s""" % events_data)

        return convert_query_to_dict("""{}""".format(events_data,))
