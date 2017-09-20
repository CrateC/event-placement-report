import os
import sys
import django

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__))))
print(PROJECT_DIR)
sys.path.append(PROJECT_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'event_placement.settings.production'
django.setup()

from events.models import Event, Platform

from django import template

register = template.Library()

@register.simple_tag
def platform_name(key):
    name = Platform.objects.filter(short_name=key).values_list('name', flat=True)[0]
    #print(name)
    return name


#platform_name('ca')
#
# @register.simple_tag
# def get_domain_url(val):
#     if 'facebook.com' in val:
#         return get_facebook_url(val)
#     else:
#         return re.sub('[\w-]+://?|(www|kiev)\.|','',val).split('/')[0]


# re.sub('[\w-]+://?|(www|kiev)\.|','',val).split('/')[0]
