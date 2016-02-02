from rest_framework import serializers
from .models import Bar,Tapa

class BarSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bar
		fields = ("nombre", "direccion", "numerovisitas",)
		
class TapaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tapa
		fields = ("bar","nombre", "votos",)

