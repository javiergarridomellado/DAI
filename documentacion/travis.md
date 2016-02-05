# Integración continua con Travis

Para el uso de Travis los pasos que se han seguido han sido:
- Registrarse en la página y sincronizar el repositorio.
- Tener un archivo de testeo de la aplicación.
- Tener un archivo manage.py que facilite la automatización del testeo.
- Tener un archivo .yml donde se le indica los pasos a seguir para cumplir con la integración continua de manera correcta y eficiente.
- En *github*, en el apartado *Setting/Webhooks&services* hay que activar el apartado de *Travis*, seguidamente se pulsa *Test Service*.

El contenido del archivo *.travis.yml* es el siguiente:
```
language: python
python:
 - "2.7"

install:
 - sudo apt-get install libmysqlclient-dev
 - pip install -r requirements.txt
script:
 - python manage.py test 
```
Por último una captura de una modificación realizada al código del repositorio:

![travis](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/travis_zpswjlfffg8.png)

# Integración continua con Snap CI

Se añade ademas un proceso de integración continua junto al despliegue en Heroku mediante [Snap-CI](https://snap-ci.com).Desde la interfaz web realizo la siguiente configuración:

![paso1](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/snapci_zpsonq9bl1n.png)

![pasotest](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/snapci_zpssudilbhg.png)

![paso2](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/snapci2_zpsnzjcntgi.png)

![paso3](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/snapci3_zpsw6xgxcjm.png)

![resultados1](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/snapciresultados3_zpsxu7gwja7.png)

![resultados2](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/snapciresultados_zpsafei2lbw.png)


Con todo esto queda realizado la integración continua, cada vez que se haga un push al repositorio se pasan los tests y si son satisfactorio se levanta la app.
