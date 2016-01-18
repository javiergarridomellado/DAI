"""
WSGI config for ProyectoDAI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
#anado
from whitenoise.django import DjangoWhiteNoise

#from dj_static import Cling
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProyectoDAI.settings")


application = get_wsgi_application()
#application = Cling(get_wsgi_application())
#anado
application = DjangoWhiteNoise(application)
