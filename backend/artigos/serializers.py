from rest_framework import serializers
from .models import Artigo, Autor

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class ArtigoGetSerializer(serializers.ModelSerializer):
    autores = AutorSerializer(many=True)
    class Meta:
        model = Artigo
        fields = ('id', 'nome', 'ano_publicacao', 'link', 'autores')

class ArtigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artigo
        fields = '__all__'
