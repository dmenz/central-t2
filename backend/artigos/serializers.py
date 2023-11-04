from rest_framework import serializers
from .models import Artigo, Autor

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class ArtigoSerializer(serializers.ModelSerializer):
    autores = serializers.SlugRelatedField(many=True, read_only=True, slug_field='nome')
    class Meta:
        model = Artigo
        fields = ('id', 'nome', 'ano_publicacao', 'link', 'autores')
