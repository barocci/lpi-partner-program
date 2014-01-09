import os
import sys

path = '/opt/lpi-partner-program/'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'lpipartners.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
