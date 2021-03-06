"""
WSGI config for blairwear project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blairwear.settings")

application = get_wsgi_application()

import blairwear.monitor
blairwear.monitor.start(interval=1.0)
