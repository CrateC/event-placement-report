from __future__ import absolute_import, unicode_literals
from celery import task, shared_task, group, chain, chord
from event_placement.celery import app
from celery.utils.log import get_task_logger
import os
import sys

from .get_view_data import get_queryset_data
try:
    from utils.query_to_dict import convert_qslist_to_dict
except:
    from utils.query_to_dict import convert_sqlite_query_to_dict

logger = get_task_logger(__name__)

@shared_task(queue='page_load')
def get_query():
    return convert_qslist_to_dict("""{}""".format(get_queryset_data(),))
