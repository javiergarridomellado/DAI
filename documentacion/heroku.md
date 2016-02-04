# Despliegue en un Paas: Heroku

Para su despliegue he necesitado de los siguientes archivos:
- [Procfile](https://github.com/javiergarridomellado/DAI/blob/master/Procfile):
```
web: gunicorn ProyectoDAI.wsgi --log-file -
```

- [runtime.txt](https://github.com/javiergarridomellado/DAI/blob/master/runtime.txt):
```
python-2.7.6
```
- [requirements.txt](https://github.com/javiergarridomellado/DAI/blob/master/requirements.txt)
```
Django==1.7
argparse==1.2.1
django-appconf==1.0.1
django-classy-tags==0.6.2
django-easy-maps==0.9.2
geopy==1.11.0
six==1.10.0
wsgiref==0.1.2
dj-database-url==0.3.0
dj-static==0.0.6
django-toolbelt==0.0.1
djangorestframework==3.3.1
foreman==0.9.7
futures==3.0.3
gunicorn==19.3.0
psycopg2==2.4.5
requests==2.8.1
requests-futures==0.9.5
static3==0.6.1
wheel==0.26.0
whitenoise==2.0.4
```
Puede verse que tambien se dispone de **whitenoise** para servir archivos estaticos (aunque hay otras maneras de realizar lo mismo, se explica a posteriori).
Tras el registro en Heroku hay que ejecutar una serie de comandos para tener apunto el despliegue:
```
wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh   
heroku login
heroku create
git add .
git commit -m "despliegue heroku"
heroku apps:rename restaurantejaviergarrido
git push heroku master
```
Cuando la aplicación se encuentre desplegada en Heroku usará la base de datos **PostgreSQL** que nos proporcionan (se define en setting.py, asi cuando la aplicación se encuentre en Heroku usara dicha base de datos), en local sigo usando **SQLite**, lo he realizado con estos pasos:
- Teniendo *psycopg2* para poder usar dicha base de datos.
- Tener instalado *dj_database_url*, tambien necesario para PostgreSQL.
- Abrir el archivo *setting.py* del proyecto y añadir lo siguiente( sacado del siguiente [enlace](http://stackoverflow.com/questions/26080303/improperlyconfigured-settings-databases-is-improperly-configured-please-supply)):
```
import dj_database_url

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
ON_HEROKU = os.environ.get('PORT')
if ON_HEROKU:
	DATABASE_URL='postgres://url_de_mi_bd'
	DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
```
- En el archivo **wsgi.py** hay que poner lo siguiente:
```
import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProyectoDAI.settings")


application = get_wsgi_application()
application = Cling(get_wsgi_application())
```
- Notar que en DATABASE_URL se pone la url de la base de datos PostgreSQL que Heroku nos ofrece, hay que darle a show para verlo.
- Subir cambios a github y hacer **git push heroku master**.
- Ejecutar los comando **heroku run python manage.py makemigrations**, **heroku run python manage.py migrate** y **heroku run python manage.py createsuperuser** para sincronizar la base de datos PostgreSQL.
 

La aplicacion [desplegada](https://restaurantejaviergarrido.herokuapp.com/restaurante/)

Si hay algun problema en algun push de heroku hacer:
```
heroku create --stack cedar
```

![app](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/appheroku_zpssfomqoh8.png)

## Como resolver los problemas de CSS en Heroku

Según la [bibliografía oficial](https://devcenter.heroku.com/articles/django-assets) estos se solucionan usando **whitenoise** en los archivos **setting.py** y **wsgi.py**, además ejecutando el comando ` python manage.py collectstatic --dry-run --noinput`.

Otra solución es la de usar **Cling** en el archivo **wsgi.py**.

En mi caso ninguna de estas me funcionó y lo solucioné sustituyendo **bootstrap** por [CDN](https://www.bootstrapcdn.com/).
Lo único que tuve que realizar fué sustituir en el template **base.html** las siguientes líneas:
```
<!--<link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="http://getbootstrap.com/examples/dashboard/dashboard.css" rel="stylesheet">-->
```

por esta:
```
<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" type="text/css">

```
