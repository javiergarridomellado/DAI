##Fabric

Como se ha comentado antes, Fabric es una biblioteca para automatizar tareas de administración o despliegues a través de SSH. Puede instalarse de varias maneras, vease:
```
$ pip install fabric
```

```
$ sudo apt-get install fabric
```

El contenido de mi archivo fabfile es el siguiente:

```
from fabric.api import run, local, hosts, cd
from fabric.contrib import django

def install_run():
	run('sudo apt-get update')
	run('sudo apt-get install -y docker.io')
	run('sudo docker pull javiergarridomellado/dai:dai')
	run('sudo docker run -i -t javiergarridomellado/dai:dai /bin/bash')
```

Puede verse en el codigo que lo que se hace es ejecutar cuatro comandos con solo una llamada, por tanto, se actualizaría el sistema base, se instalaría docker, se descargaría la imagen y se arrancaría dicho contenedor. El comando a usar es el siguiente (el archivo fabfile se encuentra en nuestra máquina y solo sirve para indicar al SSH que tiene que hacer):
```
fab -H javiergarridomellado@restaurantejaviergarrido.westeurope.cloudapp.azure.com install_run
```
Con la opcion [-H](http://www.flu-project.com/2014/03/python-y-fabric-para-administrar.html) se le indica el host, puede usarse la opcion -p para pasarle la password sino se desea introducir a posteriori, por ejemplo:
```
fab -p mipassword -H javiergarridomellado@restaurantejaviergarrido.westeurope.cloudapp.azure.com install_run
```
![ejemplodeuso](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/fabfile_zpsypeuqf79.png)

### Despligue Docker en Azure

Como es de imaginar, los pasos son breves, en concreto tres:

- El primero de ello es usar fabfile para realizar el despliegue del contenedor dentro de Azure:
```
fab -H javiergarridomellado@restaurantejaviergarrido.westeurope.cloudapp.azure.com install_run
```

![runazure](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/ifconfig_zpsknuvjham.png)

- El segundo es ejecutar el script **run_app.sh** el cual arranca la aplicación.

![run_app](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/runapp2_zpsgwj3dhoc.png)

- Por último, hay que realizar un simple NAT para que las peticiones a la máquina virtual de Azure sean respondidas por el contenedor, esto se hace de la siguiente manera:
```
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 172.17.0.1:8000
```

![nat](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/abrirpuertoazure_zpsvgmwrlyn.png)

Otra manera de realizarlo es hacer un reenvío de puertos del Docker, haber ejecutado en el fabfile la orden `docker run -t -i -p 8000:8000 javiergarridomellado/dai:dai /bin/bash` y hacer un reenvio de puertos en Azure mediante el comando `azure vm endpoint create nombremaquina 80 8000`


