from fabric.api import run, local, hosts, cd
from fabric.contrib import django


#Ejecucion de la aplicacion en modo desarrollo
def runApp():
	run('cd DAI && sudo python manage.py runserver 0.0.0.0:80')

#Actualizar la aplicacion
def actApp():
	run('cd DAI && sudo git pull')

#Realizar testeo de la aplicacion
def testApp():
	run('cd DAI && sudo python manage.py test')

#Parar servicio produccion
def stopServer():
	run('sudo service nginx stop')
	run('sudo service supervisor stop')

#Arrancar servicio produccion
def startServer():
	run('sudo service nginx start')
	run('sudo service supervisor start')

#Reiniciar servicio produccion
def restartServer():
	run('sudo service nginx restart')
	run('sudo service supervisor restart')

#Actualizar requisitos
def actRequirements():
	run('sudo pip install -r DAI/requirements.txt')

#Borrar App
def removeApp():
	run('sudo rm -f DAI')

#Clonar App
def CloneApp():
	run('sudo git clone https://github.com/javiergarridomellado/DAI.git')
