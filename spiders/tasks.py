from __future__ import absolute_import, unicode_literals
from celery import task, shared_task, group, chain, chord
from event_placement.celery import app
from celery.utils.log import get_task_logger
import os
import sys
import json
from .spiders_2 import Spiders, Parter, Concert, Karabas
from .import_db import ImportDb
from .get_facebook_events import Facebook  # request_until_succeed,process_dict
# from events.models import Platform

#
# try:
#     from parter import Parter
# except:
#     from .parter import Parter

logger = get_task_logger(__name__)

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'event_placement.settings.production'

import django
django.setup()
from events.models import Event, Platform

# from spiders.tasks import task_caribbean_parse, task_test_one, task_test_two, task_test_three, chain_caribbean, chain_chord_test


@task(ignore_result=True, queue='mainchain')
def main_chain():
    try:
        return chain(
            chord([task_caribbean_parse.si()])(task_parsed_to_db.s()),
            chord([task_parter_parse.si()])(task_parsed_to_db.s()),
            chord([task_concert_parse.si()])(task_parsed_to_db.s()),
            chord([task_karabas_parse.si()])(task_parsed_to_db.s()),
        )()
    except TypeError:
        pass

# from spiders.tasks import task_facebook_parse, task_parsed_to_db
@task(ignore_result=True, queue='todb')
def task_parsed_to_db(out_path):
    # Importing to Database
    import_ = ImportDb(out_path)
    added = import_.import_to_db()
    return added


# Main task
@task(ignore_result=True, queue='high')
def task_caribbean_parse():
    # message = "task_caribbean_parse"
    # print(message)
    l_ = Spiders()
    path = l_.start_parse()
    return path


# Tickets tasks
@task(ignore_result=True, queue='normal')
def task_parter_parse():
    l_ = Parter()
    path = l_.not_async()
    return path


@task(ignore_result=True, queue='normal')
def task_concert_parse():
    l_ = Concert()
    path = l_.not_async()
    return path


@task(ignore_result=True, queue='normal')
def task_karabas_parse():
    l_ = Karabas()
    path = l_.async()
    return path


# Facebook tasks

# from celery import chord, chain
# from spiders.tasks import fb_chain, task_parsed_to_db
# chord([task_facebook_parse.si()])(task_parsed_to_db.s())
# chord([task_facebook_parse_all.si()])(task_parsed_to_db.s())

@task(ignore_result=False, queue='mainchain')
def fb_chain():
    try:
        res = chain(
            chord([task_facebook_parse_fc.si()])(task_parsed_to_db.s()),
            chord([task_facebook_parse_fs.si()])(task_parsed_to_db.s()),
            chord([task_facebook_parse_fj.si()])(task_parsed_to_db.s()),
            chord([task_facebook_parse_fh.si()])(task_parsed_to_db.s()),
        )()
        return res.get()
    except TypeError:
        pass


queryset = Platform.objects.filter(name__startswith='fb_').values_list('short_name', flat=True)
p_names = [x for x in queryset]

@task(ignore_result=False, queue='normal')
def task_facebook_parse_fc():
    fb = Facebook(p_names[0])
    return fb.process_dict()

@task(ignore_result=False, queue='normal')
def task_facebook_parse_fs():
    fb = Facebook(p_names[1])
    return fb.process_dict()

@task(ignore_result=False, queue='normal')
def task_facebook_parse_fj():
    fb = Facebook(p_names[2])
    return fb.process_dict()

@task(ignore_result=False, queue='normal')
def task_facebook_parse_fh():
    fb = Facebook(p_names[3])
    return fb.process_dict()

@task(ignore_result=True, queue='normal')
def task_facebook_parse_all():
    #page = 'FC'
    #p_name = 'FC'
    queryset = Platform.objects.filter(name__startswith='fb_').values_list('short_name', flat=True)
    p_names = [x for x in queryset]
    for p_name in p_names:
        fb = Facebook(p_name)
        #j = json.loads(fb.request_until_succeed())
        #print(fb.process_dict(j))
        return fb.process_dict()



# Tests
@task(ignore_result=True, queue='mainchain')
def chain_chord_test():
    try:
        return chain(
            chord([task_test_one.si()])(task_test_callback.s()),
            chord([task_test_two.si()])(task_test_callback.s()),
            chord([task_test_three.si()])(task_test_callback.s())
        )()
    except TypeError:
        pass

@task(ignore_result=True, queue='normal')
def task_test_one():
    message = "HIGH_taks_home_one"
    print(message)
    return message

@task(ignore_result=True, queue='normal')
def task_test_two():
    message = "NORMAL_taks_home_one_two"
    print(message)
    # Do something...
    return message

@task(ignore_result=True, queue='normal')
def task_test_three():
    message = "LOW_taks_home_one_three"
    print(message)
    # Do something...
    return message

@task(ignore_result=True, queue='todb')
def task_test_callback(out_path):
    message = "TASK_CALLBACK: %s" % out_path
    print(message)
    # Do something...
    return message
