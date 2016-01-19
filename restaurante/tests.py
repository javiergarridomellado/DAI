from django.test import TestCase

# Create your tests here.


from restaurante.views import *
from restaurante.models import Bar,Tapa
from django.test.client import RequestFactory
# Create your tests here.Anadido testeo rutas



class BarMethodTests(TestCase):

	def test_nombre_bar(self):
		bar = Bar(nombre='BarPaco' ,direccion='Recogidas', numerovisitas='500')
		bar.save()
		self.assertEqual(bar.nombre,'BarPaco')
		self.assertEqual(bar.direccion,'Recogidas')
		self.assertEqual(bar.numerovisitas,'500')
		print("Testeo correcto.")

	def setUp(self):
		Bar.objects.create(nombre="BarVietto", direccion="Granada",numerovisitas='500')
		Bar.objects.create(nombre="BarPaco", direccion="Albolote",numerovisitas='500')

	def test_bar_ciudad(self):
		bVietto = Bar.objects.get(nombre="BarVietto")
		bPaco = Bar.objects.get(nombre="BarPaco")
		self.assertEqual(bVietto.direccion,'Granada')
		self.assertEqual(bPaco.direccion,'Albolote')
		print("Testeo correcto.")
