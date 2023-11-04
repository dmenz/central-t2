from rest_framework.views import APIView
from artigos.models import Autor, Artigo
from artigos.serializers import AutorSerializer, ArtigoSerializer
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ArtigoView(APIView):

    @swagger_auto_schema()
    def post(self, request):
        pass
    
    @swagger_auto_schema()
    def put(self, request, id_arg):
        pass


# Função para combinar as entradas dos campos de busca para filtrar os
# resultados da busca.
def le_parametros_filtro(request):
        filterquery = {}
        try:
            titulo = request.GET['titulo']
            if titulo:
                filterquery['nome__icontains'] = titulo
        except:
            pass
        try:
            autor = request.GET['autor']
            if autor:
                filterquery['autores__nome__icontains'] = autor
        except:
            pass
        return filterquery


class ArtigosView(APIView):
    
    @swagger_auto_schema(
        operation_summary='Lista todos os artigos',
        operation_description="Obter informações sobre todos os artigos",
        manual_parameters = [ 
            openapi.Parameter(
                name='titulo',
                in_=openapi.IN_QUERY,
                type='string',
                required=False,),
            openapi.Parameter(
                name='autor',
                in_=openapi.IN_QUERY,
                type='string',
                required=False,)
            ],
        request_body=None, # opcional
        responses={200: ArtigoSerializer(many=True)}
    )
    def get(self, request):
        parametros = le_parametros_filtro(request)
        queryset = Artigo.objects.all().filter(**parametros)
        serializer = ArtigoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(('DELETE',))
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(
    )
    def delete(self, request):
        pass


class AutorView(APIView):
    @swagger_auto_schema()
    def get(self, request):
        pass

    @swagger_auto_schema()
    def post(self, request):
        pass

    @swagger_auto_schema()
    def put(self, request):
        pass

    @swagger_auto_schema()
    def delete(self, request):
        pass
    

class AutoresView(APIView):
    @swagger_auto_schema(
        operation_summary='Lista todos os autores',
        operation_description="Obter informações sobre todos os autores",
        manual_parameters = [ 
            openapi.Parameter(
                name='autor',
                in_=openapi.IN_QUERY,
                type='string',
                required=False,),
            ],
        request_body=None, # opcional
        responses={200: AutorSerializer(many=True)}
    )
    def get(self, request):
        parametros = le_parametros_filtro(request)
        queryset = Autor.objects.all().filter(**parametros)
        serializer = AutorSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
