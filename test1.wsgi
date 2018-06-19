import os
import sys
import site
import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'appliedpingdom.settings'
site.addsitedir('/srv/my_app_venv/lib/python2.7/site-packages')
sys.path.append('/srv/Web_Tracker')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

