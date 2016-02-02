# ProyIVDAI_FJGM
Autor: Francisco Javier Garrido Mellado

[![Build Status](https://travis-ci.org/javiergarridomellado/DAI.svg?branch=master)](https://travis-ci.org/javiergarridomellado/DAI)

[![Build Status](https://snap-ci.com/javiergarridomellado/DAI/branch/master/build_image)](https://snap-ci.com/javiergarridomellado/DAI/branch/master)

[![Heroku](https://www.herokucdn.com/deploy/button.png)](https://restaurantejaviergarrido.herokuapp.com/restaurante/)

[![Docker](https://camo.githubusercontent.com/8a4737bc02fcfeb36a2d7cfb9d3e886e9baf37ad/687474703a2f2f693632382e70686f746f6275636b65742e636f6d2f616c62756d732f7575362f726f6d696c67696c646f2f646f636b657269636f6e5f7a7073776a3369667772772e706e67)](https://hub.docker.com/r/javiergarridomellado/dai/)

[![Azure](https://camo.githubusercontent.com/0a0a0d99a96e23a0af8b612b45cf0e204080ad6c/68747470733a2f2f7777772e64726f70626f782e636f6d2f732f6f717572366b3730706f797363786a2f617a7572652e706e673f646c3d31)](http://restaurantejaviergarrido.cloudapp.net/restaurante/)


## Introducción Proyecto Restaurante 

Se trata de  una aplicación de Bares(tambien restaurantes) y Tapas donde los usuarios se registran e introducen su bar con sus correspondientes tapas, además se les permite votar ( solo es necesario estar registrados ) las tapas que más le ha gustado. La página muestra una gráfica de los Bares más exitosos así como un mapa de Google para que el usuario pueda visitarlo fisicamente.

Este proyecto se ha llevado a cabo conjuntamente con la asignatura de Diseño de Aplicaciones para Internet.

[Inscrito en el certamen de Software Libre](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/Pantallazo-Gracias%20-%20Chromium_zpsjdau6lfd.png)

## Seguridad

Respecto a la seguridad se garantiza que los datos y credenciales de los usuarios quedan salvaguardados de cualquier ataque, para ello se ha usado un sistema criptográfico basado en hashes(**SHA 256**) que garantiza la autenticidad e integridad.

## Infraestructura

Se creará en la nube la infraestructura necesaria para la aplicación, siendo necesario el provisionamiento y la instalación de diferentes librerías para su correcto funcionamiento.

Resumen:
-	1.Sistema web donde interaccionan varios usuarios.
-	2.Servidores web.
-	3.Base de datos.


##Herramienta de Construcción

Python permite como herramienta de construcción el uso del archivo *manage.py* , es el que he usado en mi caso, puede verse en [travis](https://travis-ci.org) y [snap-ci](https://snap-ci.com/) como lo uso para la construcción y el posterior testeo.

Además se añaden los archivos [create_and_run](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIV/create_and_run.sh), [docker_install_and_run](https://github.com/javiergarridomellado/DAI/blob/master/scripts/docker_install_and_run.sh), [heroku_deploy](https://github.com/javiergarridomellado/DAI/blob/master/scripts/heroku_deploy.sh) y [run_app](https://github.com/javiergarridomellado/DAI/blob/master/scripts/run_app.sh) para el despligue automático en una máquina virtual de Azure( inclusive la posibilidad de despliegue en una máquina local de [VirtualBox](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIVLocal/create_and_run.sh) ), la construcción de un entorno seguro (contenedor Docker), su posterior despliegue automático en el PAAS de Heroku y el arranque de la aplicación en local respectivamente.

## Instalación local de la aplicación

Para ello basta con ejecutar los siguientes comandos:
```
$ git clone https://github.com/javiergarridomellado/DAI.git
$ cd DAI
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

##Desarrollo basado en pruebas

Para las pruebas he usado el sistema de testeo de Django. Basta con ejecutar el siguiente comando:

**python manage.py test** ó **python manage.py test nombreaplicacion**

Puede verse los correspondientes [tests](https://github.com/javiergarridomellado/DAI/blob/master/restaurante/tests.py) que se realizan.Se usan tanto para **travis** como para **snap-ci**.

![tests](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/travis_zpstciokpes.png)

##Integración continua

En este paso he elegido dos sistemas de integración continua de modo que cada cambio que realice implique una ejecución de los tests mencionados anteriormente, de esta manera se comprueba que la aplicación sigue funcionando correctamente.

En mi caso, he realizado la integración continua con [Travis](https://travis-ci.org/javiergarridomellado/DAI) y con [snap-ci](https://snap-ci.com/javiergarridomellado/DAI/branch/master) ya que me parecieron sencillos y muy completos.


[Más información](https://github.com/javiergarridomellado/DAI/blob/master/documentacion/travis.md)

## Despliegue en un Paas Heroku

Me he decantado por Heroku por la facilidad para el despliegue y porque es la que pedían en los ejercicios de la relación.
Esta es la aplicación desplegada en Heroku: [https://restaurantejaviergarrido.herokuapp.com/restaurante/](https://restaurantejaviergarrido.herokuapp.com/restaurante/)

Se ha automatizado el despliegue en heroku con el script [heroku_deploy](https://github.com/javiergarridomellado/DAI/blob/master/scripts/heroku_deploy.sh)

[Más información](https://github.com/javiergarridomellado/DAI/blob/master/documentacion/heroku.md)
 

## Despliegue remoto: Fabric

Con la ayuda de [Fabric](http://www.fabfile.org/), que es una biblioteca de Python para automatizar tareas de administración haciendo uso de SSH, he creado un entorno de pruebas en una [máquina virtual de Azure](https://azure.microsoft.com/es-es/).

La creación del entorno Docker en Azure usando el archivo [fabfile](https://github.com/javiergarridomellado/DAI/blob/master/fabfile.py) puede consultarse [aqui](https://github.com/javiergarridomellado/DAI/blob/master/documentacion/fabfile.md).

Como he creado la máquina virtual puede [consultarse](https://github.com/javiergarridomellado/DAI/blob/master/documentacion/azure.md).

La aplicación ( del Docker ) desplegada es la siguiente [http://restaurantejaviergarrido.westeurope.cloudapp.azure.com/restaurante/](http://restaurantejaviergarrido.westeurope.cloudapp.azure.com/).

## Entorno de pruebas:[Docker](https://www.docker.com/)

Se usa Docker como plataforma que automatiza el despliegue de la aplicación dentro de contenedores software, de manera que pueda probarse en un entorno aislado antes de desplegarla a producción.

La imagen de la aplicación es la [siguiente](https://hub.docker.com/r/javiergarridomellado/dai/)

Para crear el entorno de prueba se ha provisto del archivo **docker_install_and_run.sh**(explicado en el siguiente apartado), basta con ejecutar:
```
./docker_install_and_run.sh
```
Sino se desea usar el script puede descargarse la imagen directamente ejecutando:
 ```
sudo docker run -t -i javiergarridomellado/dai:dai /bin/bash
```
Para mayor comodidad se puede hacer un reenvio de puertos de la siguiente manera( esto evita tener que buscar la ip del docker ):
```
docker run -t -i -p 8000:8000 javiergarridomellado/dai:dai /bin/bash
```

[Más información](https://github.com/javiergarridomellado/DAI/blob/master/documentacion/docker.md)

![reenv](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/reenv_zpsrts3yndc.png)

### Automatización o Modo de Uso ( Online )

Consultar el apartado de [Despliegue Remoto](https://github.com/javiergarridomellado/DAI/blob/master/documentacion/fabfile.md).

Notar que se ha añadido un script [heroku_deploy.sh](https://github.com/javiergarridomellado/DAI/blob/master/scripts/heroku_deploy.sh) el cual despliega la aplicación en el PaaS Heroku siempre y cuando las pruebas en el entorno seguro de Docker hayan sido satisfactorias. Dicho script se encuentra en `DAI/scripts`.



### Automatización o Modo de Uso ( Local )

Para facilitar el uso de la aplicación se han añadido tres [scripts](https://github.com/javiergarridomellado/DAI/tree/master/scripts) de manera que cualquier persona con un conocimento básico pueda probarla en un entorno tanto aislado como online.

Los pasos a seguir son los siguientes:

- Clonar o copiar el contenido del archivo [docker_install_and_run.sh](https://github.com/javiergarridomellado/DAI/blob/master/scripts/docker_install_and_run.sh) en un archivo **.sh**
- Dar permisos de ejecución mediante la orden **chmod**, por ejemplo `chmod 777 docker_install_and_run.sh`
- Ejecutar el archivo mediante la orden `./docker_install_and_run.sh`

Con esto nos encontramos dentro de la imagen descargada, la cual tiene la aplicación dentro. Hecho esto, hay que teclear `cd DAI/scripts` y se nos abre un abanico de dos posibilidades:

![dockerrun](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/dokerrun_zpsatftkyxx.png)

#### Ejecución 

De esta manera se ejecuta la aplicación de manera local(obviamente aislado del sistema anfitrión ya que se encuentra dentro del contenedor):
- Ejecutar la orden `ifconfig` para conocer la IP que hay que poner en el navegador.
- Dar permisos de ejecución mediante la orden **chmod** al archivo [run_app.sh](https://github.com/javiergarridomellado/DAI/blob/master/scripts/run_app.sh), por ejemplo `chmod 777 run_app.sh`
- Ejecutar el archivo mediante la orden `./run_app.sh`
- Ingresar en el navegador anfitrión `ip_del_contenedor:8000` , con ello tendremos la aplicación lanzada( existe la opción de reenvio de puertos para Docker como he comentado antes).

![ifconfig](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/ifconfig_zpsvfisjtvf.png)

![runapp](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/runapp2_zpsbvabmpl8.png)

![nav](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/dockerappdesplegadalocal_zpsrkuj1kx3.png)

#### Despliegue en Paas

De esta manera se despliega la aplicación en el PaaS Heroku (obviamente es interesante realizar el paso anterior y probar la aplicación en dicho entorno aislado antes de desplegarlo) y se utiliza la base de datos PostgreSQL que nos proporciona Heroku:
- Dar permisos de ejecución mediante la orden **chmod** al archivo [heroku_deploy.sh](https://github.com/javiergarridomellado/DAI/blob/master/scripts/heroku_deploy.sh), por ejemplo `chmod 777 heroku_deploy.sh`
- Ejecutar el archivo mediante la orden `./heroku_deploy.sh`
- Ingresar el user/password de nuestra cuenta Heroku y automaticamente la aplicación queda desplegada.

![herokudeploy](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/herokudeploy_zpsel51zwvq.png)

![user](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/her_zpsp25ztb4u.png)

## Despliegue en un Iaas: Azure

He usado Azure como IaaS. La aplicación se despliega automáticamente y queda en modo producción ejecutando el script [create_and_run](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIV/create_and_run.sh) gracias a Vagrant y Ansible. Se recomienda definir la variable de entorno ejecutando `export ANSIBLE_HOSTS=~/ruta/ansible_hosts`.
La url donde puede verse la aplicación la proporciona Azure al crear la máquina en la nube y es la siguiente [http://restaurantejaviergarrido.cloudapp.net/restaurante/](http://restaurantejaviergarrido.cloudapp.net/restaurante/)( Ahora se encuentra apagada).

```
./create_and_run.sh
```
Los servicios utilizados en modo producción son los siguientes:

- [Azure](https://azure.microsoft.com/en-us/?b=16.01) como IaaS ( servicio en la nube).
- [MySQL](https://www.mysql.com/) como servidor de base de datos.
- [Nginx](http://nginx.org/) como servidor web( responde las peticiones estáticas como principal función del servidor ).
- [Gunicorn](http://gunicorn.org/) como servidor web( es el servidor de la aplicación y responde a las peticiones dinámicas ).
- [Supervisor](http://supervisord.org/) como **watchdog**( monitoriza y mantiene en continuo funcionamiento el servidor Gunicorn )

**Nota: Para ejecutar el script es necesario tener en el mismo nivel los archivos [Vagrantfile](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIV/Vagrantfile), [ansible_hosts](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIV/ansible_hosts) e [iv.yml](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIV/iv.yml) que se encuentran en el siguiente [directorio](https://github.com/javiergarridomellado/DAI/tree/master/VagrantIV)**

[Más información](https://github.com/javiergarridomellado/DAI/blob/master/documentacion/despliegueAzure.md)

![appdespl](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/appdespleazure_zps0wzccsgy.png)

### Despliegue en VirtualBox

Debido a que no todo el mundo dispone de cuenta en Azure facilito la opción del despliegue en local gracias a VirtualBox, para ello al igual que antes se define la variable de entorno `export ANSIBLE_HOSTS=~/ruta/ansible_hosts` y ya solo basta con ejecutar el scrip [create_and_run](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIVLocal/create_and_run.sh).

```
./create_and_run.sh
```
Los servicios utilizados en modo producción son los siguientes:

- [VirtualBox](https://www.virtualbox.org/) como software de virtualización local.
- [MySQL](https://www.mysql.com/) como servidor de base de datos.
- [Nginx](http://nginx.org/) como servidor web( responde las peticiones estáticas como principal función del servidor ).
- [Gunicorn](http://gunicorn.org/) como servidor web( es el servidor de la aplicación y responde a las peticiones dinámicas ).
- [Supervisor](http://supervisord.org/) como **watchdog**( monitoriza y mantiene en continuo funcionamiento el servidor Gunicorn )

**Nota: Para ejecutar el script es necesario tener en el mismo nivel los archivos [Vagrantfile](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIVLocal/Vagrantfile), [ansible_hosts](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIVLocal/ansible_hosts) e [iv.yml](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIVLocal/iv.yml) que se encuentran en el siguiente [directorio](https://github.com/javiergarridomellado/DAI/tree/master/VagrantIVLocal)**

[Más información](https://github.com/javiergarridomellado/DAI/blob/master/documentacion/despliegueVB.md)



##Generacion de Documentación
- Ingresar en el directorio **/apu**
- Ejecutar en el terminal **epydoc --html views.py models.py**


## Cambios Realizados

Se ha añade un [fichero](https://github.com/javiergarridomellado/DAI/blob/master/documentacion/cambios.md) donde se comentan los cambios más relevantes entre los diferentes hitos para facilitar la corrección de la práctica.

## Comandos Básicos

###Despliegue en Azure o VirtualBox
```
$ ./create_and_run.sh
```

###Instalar dependencias
```
$ pip install -r requirements.txt
```

###Sincronizar base de datos
```
$ python manage.py migrate --noinput
```

###Test
```
$ python manage.py test
```

###Arrancar aplicación( 2 opciones )
```
$ ./run_app.sh
```

```
$ python manage.py runserver
```

###Despliegue en heroku
```
$ ./heroku_deploy.sh
```

###Instalar imagen docker(Contenedor Ubuntu+Aplicación)
```
$ ./docker_install_and_run.sh
```

## Referencias

- [Documentación oficial de Azure](https://azure.microsoft.com/es-es/documentation/)
- [Documentación oficial de Ansible](http://docs.ansible.com/)
- [Documentación oficial de Vagrant](https://www.vagrantup.com/docs/)
- [Documentación oficial de MySQL](https://dev.mysql.com/doc/)
- [Documentación oficial de Nginx](http://nginx.org/en/docs/)
- [Documentación oficial de Gunicorn](http://docs.gunicorn.org/en/stable/run.html)
- [Documentación oficial de Supervisor](http://supervisord.org/index.html)
- [Documentación oficial de Docker](https://docs.docker.com/)
- [Documentación oficial de Fabfile](http://docs.fabfile.org/en/1.10/)
- [Documentación oficial de Heroku](https://devcenter.heroku.com/categories/reference)
- [Documentación oficial de Snap-ci](https://docs.snap-ci.com/getting-started/)
- [Documentación oficial de Travis](https://docs.travis-ci.com/)
- [Documentación oficial de Django](https://docs.djangoproject.com/en/1.9/)


