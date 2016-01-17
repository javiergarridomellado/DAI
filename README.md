# ProyIVDAI_FJGM
Autor: Francisco Javier Garrido Mellado

[![Build Status](https://travis-ci.org/javiergarridomellado/IV_javiergarridomellado.svg?branch=master)](https://travis-ci.org/javiergarridomellado/IV_javiergarridomellado)

[![Build Status](https://snap-ci.com/javiergarridomellado/IV_javiergarridomellado/branch/master/build_image)](https://snap-ci.com/javiergarridomellado/IV_javiergarridomellado/branch/master)

[![Heroku](https://www.herokucdn.com/deploy/button.png)](https://apuestas.herokuapp.com/)


## Introducción Proyecto Apuestas

Se trata de  una aplicación de apuestas de fútbol donde los usuarios registran unos datos básicos y disponen de un fondo para apostar, debates, novedades sobre fútbol, etc. 

Este proyecto será llevado a lo largo del año conjuntamente con la asignatura de Diseño de Aplicaciones para Internet.

[Inscrito en el certamen de Software Libre](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/Pantallazo-Gracias%20-%20Chromium_zpsjdau6lfd.png)

## Seguridad

Respecto a la seguridad se implementará de manera que los datos y credenciales de los usuarios queden salvaguardados de cualquier ataque, para ello será necesario que estos esten separados.

## Infraestructura

Se creará en la nube la infraestructura necesaria para la aplicación, siendo necesario servidores web con su correspondiente balanceador y servidores de bases de datos MySQL replicadas.

Resumen:
-	1.Sistema web donde interaccionan varios usuarios.
-	2.Servidores web con su correspondiente balanceador.
-	3.Base de datos replicadas.


##Herramienta de Construcción

Python permite como herramienta de construcción el uso del archivo *manage.py* , es el que he usado en mi caso, puede verse en travis y snap-ci como lo uso para la construcción y el posterior testeo.

Además se añaden los archivos [docker_install_and_run](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/scripts/docker_install_and_run.sh), [heroku_deploy](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/scripts/heroku_deploy.sh) y [run_app](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/scripts/run_app.sh) para la construcción de un entorno seguro (contenedor Docker), su posterior despliegue automático en el PAAS de Heroku y el arranque de la aplicación en local.

## Instalación local de la aplicación

Para ello basta con ejecutar los siguientes comandos:
```
$ git clone https://github.com/javiergarridomellado/IV_javiergarridomellado.git
$ cd IV_javiergarridomellado
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

##Desarrollo basado en pruebas

Para las pruebas he usado el sistema de testeo de Django. Basta con ejecutar el siguiente comando:

**python manage.py test** ó **python manage.py test nombreaplicacion**

Puede verse los correspondientes [tests](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/apu/tests.py) que se realizan.Se usan tanto para **travis** como para **snap-ci**.

![tests](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/tests_zpstcqojtb8.png)

##Integración continua

En este paso he elegido dos sistemas de integración continua de modo que cada cambio que se realice implique una ejecución de los tests mencionados anteriormente, de esta manera se comprueba que la aplicación sigue funcionando correctamente.

En mi caso, he realizado la integración continua con [Travis](https://travis-ci.org/javiergarridomellado/IV_javiergarridomellado) y con [snap-ci](https://snap-ci.com/javiergarridomellado/IV_javiergarridomellado/branch/master) ya que me parecieron sencillos y muy completos.


[Más información](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/documentacion/travis.md)

## Despliegue en un Paas Heroku

Me he decantado por Heroku por la facilidad para el despliegue y porque es la que pedían en los ejercicios de la relación.
Esta es la aplicación desplegada en Heroku: [https://apuestas.herokuapp.com/](https://apuestas.herokuapp.com/)

Se ha automatizado el despliegue en heroku con el script [heroku_deploy](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/scripts/heroku_deploy.sh)

[Más información](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/documentacion/heroku.md)
 

## Despliegue remoto: Fabric

Con la ayuda de [Fabric](http://www.fabfile.org/), que es una biblioteca de Python para automatizar tareas de administración haciendo uso de SSH, he creado un entorno de pruebas en una [máquina virtual de Azure](https://azure.microsoft.com/es-es/).

La creación del entorno Docker en Azure usando el archivo [fabfile](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/fabfile.py) puede consultarse [aqui](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/documentacion/fabfile.md).

Como he creado la máquina virtual puede [consultarse](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/documentacion/azure.md).

La aplicación ( del Docker ) desplegada es la siguiente [http://apuestas.westeurope.cloudapp.azure.com/](http://apuestas.westeurope.cloudapp.azure.com/).

## Entorno de pruebas:[Docker](https://www.docker.com/)

Se usa Docker como plataforma que automatiza el despliegue de la aplicación dentro de contenedores software, de manera que pueda probarse en un entorno aislado antes de desplegarla a producción.

La imagen de la aplicación es la [siguiente](https://hub.docker.com/r/javiergarridomellado/iv_javiergarridomellado/)

Para crear el entorno de prueba se ha provisto del archivo **docker_install_and_run.sh**(explicado en el siguiente apartado), basta con ejecutar:
```
./docker_install_and_run.sh
```
Sino se desea usar el script puede descargarse la imagen directamente ejecutando:
 ```
sudo docker run -t -i javiergarridomellado/iv_javiergarridomellado:apuestas /bin/bash
```

[Más información](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/documentacion/docker.md)


## Automatización o Modo de Uso ( Online )

Consultar el apartado de [Despliegue Remoto](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/documentacion/fabfile.md).

Notar que se ha añadido un script [heroku_deploy.sh](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/scripts/heroku_deploy.sh) el cual despliega la aplicación en el PaaS Heroku siempre y cuando las pruebas en el entorno seguro de Docker hayan sido satisfactorias. Dicho script se encuentra en `IV_javiergarridomellado/scripts`.



## Automatización o Modo de Uso ( Local )

Para facilitar el uso de la aplicación se han añadido tres [scripts](https://github.com/javiergarridomellado/IV_javiergarridomellado/tree/master/scripts) de manera que cualquier persona con un conocimento básico pueda probarla en un entorno tanto aislado como online.

Los pasos a seguir son los siguientes:

- Clonar o copiar el contenido del archivo [docker_install_and_run.sh](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/scripts/docker_install_and_run.sh) en un archivo **.sh**
- Dar permisos de ejecución mediante la orden **chmod**, por ejemplo `chmod 777 docker_install_and_run.sh`
- Ejecutar el archivo mediante la orden `./docker_install_and_run.sh`

Con esto nos encontramos dentro de la imagen descargada, la cual tiene la aplicación dentro. Hecho esto, hay que teclear `cd IV_javiergarridomellado/scripts` y se nos abre un abanico de dos posibilidades:
gi
![dockerrun](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/dockerrun_zpsvewnjp9u.png)

### Ejecución 

De esta manera se ejecuta la aplicación de manera local(obviamente aislado del sistema anfitrión ya que se encuentra dentro del contenedor):
- Ejecutar la orden `ifconfig` para conocer la IP que hay que poner en el navegador.
- Dar permisos de ejecución mediante la orden **chmod** al archivo [run_app.sh](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/scripts/run_app.sh), por ejemplo `chmod 777 run_app.sh`
- Ejecutar el archivo mediante la orden `./run_app.sh`
- Ingresar en el navegador anfitrión `ip_del_contenedor:8000` , con ello tendremos la aplicación lanzada.

![ifconfig](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/ifconfig_zps6z0uav6o.png)

![runapp](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/runapp_zpsnsa9qlud.png)

![nav](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/nav_zpsx1vfvbbm.png)

### Despliegue en Paas

De esta manera se despliega la aplicación en el PaaS Heroku (obviamente es interesante realizar el paso anterior y probar la aplicación en dicho entorno aislado antes de desplegarlo) y se utiliza la base de datos PostgreSQL que nos proporciona Heroku:
- Dar permisos de ejecución mediante la orden **chmod** al archivo [heroku_deploy.sh](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/scripts/heroku_deploy.sh), por ejemplo `chmod 777 heroku_deploy.sh`
- Ejecutar el archivo mediante la orden `./heroku_deploy.sh`
- Ingresar el user/password de nuestra cuenta Heroku y automaticamente la aplicación queda desplegada.

![herokudeploy](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/herokudeploy_zpsnx8ryz6s.png)

![user](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/her_zpsp25ztb4u.png)

## Despliegue en un Iaas: Azure

He usado Azure como IaaS. La aplicación se despliega automáticamente ejecutando el script [create_and_run](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantAzure/create_and_run.sh) gracias a Vagrant y Ansible. Se recomienda antes definir la variable de entorno ejecutando `export ANSIBLE_HOSTS=~/ruta/ansible_hosts`.
La url donde puede verse la aplicación la proporciona Azure al crear la máquina en la nube y es la siguiente [apuestas.cloudapp.net](apuestas.cloudapp.net)( Ahora se encuentra apagada).

```
./create_and_run.sh
```

**Nota: Para ejecutar el script es necesario tener en el mismo nivel los archivos [Vagrantfile](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantAzure/Vagrantfile), [ansible_hosts](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantAzure/ansible_hosts) e [iv.yml](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantAzure/iv.yml) que se encuentran en el siguiente [directorio](https://github.com/javiergarridomellado/IV_javiergarridomellado/tree/master/VagrantAzure)**

[Más información](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/documentacion/despliegueAzure.md)

### Despliegue en VirtualBox

Debido a que no todo el mundo dispone de cuenta en Azure facilito la opción del despliegue en local gracias a VirtualBox, para ello al igual que antes se define la variable de entorno `export ANSIBLE_HOSTS=~/ruta/ansible_hosts` y ya solo basta con ejecutar el scrip [create_and_run](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantLocal/create_and_run.sh).

```
./create_and_run.sh
```

**Nota: Para ejecutar el script es necesario tener en el mismo nivel los archivos [Vagrantfile](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantLocal/Vagrantfile), [ansible_hosts](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantLocal/ansible_hosts) e [iv.yml](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantLocal/iv.yml) que se encuentran en el siguiente [directorio](https://github.com/javiergarridomellado/IV_javiergarridomellado/tree/master/VagrantLocal)**

[Más información](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/documentacion/despliegueVB.md)



##Generacion de Documentación
- Ingresar en el directorio **/apu**
- Ejecutar en el terminal **epydoc --html views.py models.py**


## Cambios Realizados

Se ha añade un [fichero](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/documentacion/cambios.md) donde se comentan los cambios más relevantes entre los diferentes hitos para facilitar la corrección de la práctica.

## Comandos Básicos

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



