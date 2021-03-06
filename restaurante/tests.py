from django.test import TestCase

# Create your tests here.


from restaurante.views import *
from restaurante.models import Bar,Tapa
from django.test.client import RequestFactory
# Create your tests here.Anadido testeo rutas




class BarMethodTests(TestCase):

	#def test_nombre_bar(self):
		#bar = Bar(nombre='BarPaco' ,direccion='Recogidas', numerovisitas='500')
		#bar.save()
		#self.assertEqual(bar.nombre,'BarPaco')
		#self.assertEqual(bar.direccion,'Recogidas')
		#self.assertEqual(bar.numerovisitas,'500')
		#print("Testeo correcto.")

	def setUp(self):
		Bar.objects.create(nombre="BarVietto", direccion="Granada",numerovisitas='500')
		Bar.objects.create(nombre="BarPaco", direccion="Albolote",numerovisitas='500')

	def test_bar_ciudad(self):
		bVietto = Bar.objects.get(nombre="BarVietto")
		bPaco = Bar.objects.get(nombre="BarPaco")
		self.assertEqual(bVietto.direccion,'Granada')
		self.assertEqual(bPaco.direccion,'Albolote')
		print("Testeo de Bar correcto.")

class TapaMethodTests(TestCase):


	def setUp(self):
		bPaco = Bar(nombre='BarPaco' ,direccion='Granada', numerovisitas='500')
		bPaco.save()
		bVietto = Bar(nombre='BarVietto' ,direccion='Albolote', numerovisitas='500')
		bVietto.save()
		Tapa.objects.create(nombre="Hamburguesa", bar=bPaco, votos='35')
		Tapa.objects.create(nombre="Pipas", bar=bVietto, votos='25')

	def test_tapa_bar(self):
		Hamb = Tapa.objects.get(nombre="Hamburguesa", votos='35')
		Pip = Tapa.objects.get(nombre="Pipas", votos='25')
		bVietto = Bar.objects.get(nombre="BarVietto")
		bPaco = Bar.objects.get(nombre="BarPaco")
		self.assertEqual(Hamb.bar,bPaco)
		self.assertEqual(Pip.bar,bVietto)
		print("Testeo de pertenencia correcto.")

from rest_framework import status
from rest_framework.test import APITestCase

class BarREST(APITestCase):
	def test_creacion_bar(self):
		data = {"nombre" : "testeo", "direccion" : "direccion", "numerovisitas" : 50 }
		response= self.client.post("/restaurante/listado_bares/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Bar.objects.get().nombre, "testeo")
		print("Creacion de BAR correcta con interfaz REST")
		
	def test_mostrar_bares(self):
		bar1 = Bar(nombre="testeo", direccion="direccion", numerovisitas=50)
		bar1.save()
		bar2 = Bar(nombre="testeo2", direccion="direccion2", numerovisitas=100)
		bar2.save()
		response = self.client.get("/restaurante/listado_bares/")
		self.assertEqual(response.content, b'[{"nombre":"testeo","direccion":"direccion","numerovisitas":50},{"nombre":"testeo2","direccion":"direccion2","numerovisitas":100}]')
		print("Listado de BARES OK mediante interfaz REST")
