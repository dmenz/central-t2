from rest_framework.views import APIView
from artigos.models import Autor, Artigo
from artigos.serializers import ArtigoSerializer, AutorSerializer, ArtigoGetSerializer
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class ArtigoIdView(APIView):
    @swagger_auto_schema(
        operation_summary='Dados de um artigo',
        operation_description="Obter informações sobre um artigo específico",
        responses={
            200: ArtigoSerializer(),
            400: 'Mensagem de erro',
        },
        manual_parameters=[
            openapi.Parameter('id',in_=openapi.IN_PATH,
                default=5,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='id do artigo na URL',
            ),
        ],
    )
    def get(self, request, id):
        try:
            queryset = Artigo.objects.get(id=id)
            serializer = ArtigoGetSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'msg': f'Artigo com id #{id} não existe'},
                            status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary='Atualiza artigo', operation_description="Atualizar um artigo existente",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nome': openapi.Schema(
                    example='Artigo 1', 
                    description='Título do artigo',
                    type=openapi.TYPE_STRING,
                    ),
                'ano_publicacao': openapi.Schema(
                    example='2023',
                    description='Ano de publicação',
                    type=openapi.TYPE_STRING,
                    ),
                'autores': openapi.Schema(
                    example=[1,2],
                    description='IDs dos autores do artigo',
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER)),
                'link': openapi.Schema(
                    example='https://www.google.com',
                    description='Link',
                    type=openapi.TYPE_STRING
                    ),
            },
        ),
        responses={200: ArtigoSerializer(), 400: ArtigoSerializer(), },
        manual_parameters=[
            openapi.Parameter('id',openapi.IN_PATH, default=41, type=openapi.TYPE_INTEGER,
                required=True, description='id do artigo na URL',),
        ],
    )
    def put(self, request, id):
        '''
        Atualiza os dados de um artigo.
        O ID do artigo a ser atualizado vem pela URL.'''
        try:
            carro = Artigo.objects.get(id=id)
            serializer = ArtigoSerializer(carro, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Artigo.DoesNotExist:
            return Response({'msg': f'Artigo com id #{id} não existe'},
                            status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary='Deleta artigo',
        operation_description="Deletar um artigo existente",
        responses={
            204: 'Sem conteúdo',
            404: 'Mensagem de erro',
        },
        manual_parameters=[
            openapi.Parameter('id',openapi.IN_PATH, default=14,
                type=openapi.TYPE_INTEGER, required=True,
                description='id do artigo na URL',),
        ],
    )
    def delete(self, request, id):
        '''
        Deleta um artigo.
        O ID do artigo a ser deletado vem pela URL.'''
        try:
            carro = Artigo.objects.get(id=id)
            carro.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Artigo.DoesNotExist:
            return Response({'msg': f'Artigo com id #{id} não existe'},
                            status.HTTP_404_NOT_FOUND)


class ArtigoView(APIView):
    @swagger_auto_schema(
        operation_summary='Criar artigo',
        operation_description="Criar um novo artigo",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nome': openapi.Schema(
                    example='Artigo 1', 
                    description='Título do artigo',
                    type=openapi.TYPE_STRING,
                    ),
                'ano_publicacao': openapi.Schema(
                    example='2023',
                    description='Ano de publicação',
                    type=openapi.TYPE_STRING,
                    ),
                'autores': openapi.Schema(
                    example=[14,16],
                    description='IDs dos autores do artigo',
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER)),
                'link': openapi.Schema(
                    example='https://www.google.com',
                    description='Link',
                    type=openapi.TYPE_STRING
                    ),
            },
            required=['nome', 'ano_publicacao', 'autores'],
        ),
        responses={201: ArtigoSerializer(), 400: 'Dados errados',},
    )
    def post(self, request):
        serializer = ArtigoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


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
        responses={200: ArtigoGetSerializer(many=True)}
    )
    def get(self, request):
        parametros = le_parametros_filtro(request)
        queryset = Artigo.objects.all().filter(**parametros)
        serializer = ArtigoGetSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AutorView(APIView):
    @swagger_auto_schema()
    def get(self, request):
        pass

    @swagger_auto_schema()
    def post(self, request):
        serializer = AutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        request_body=None, # opcional
        responses={200: AutorSerializer(many=True)}
    )
    def get(self, request):
        queryset = Autor.objects.all()
        serializer = AutorSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
