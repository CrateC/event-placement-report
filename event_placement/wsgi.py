"""
WSGI config for event_placement project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["DJANGO_SETTINGS_MODULE"] = 'event_placement.settings.production'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_placement.settings.production")

application = get_wsgi_application()
