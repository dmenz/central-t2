from rest_framework.views import APIView
from artigos.models import Autor, Artigo
from artigos.serializers import ArtigoSerializer, AutorSerializer, ArtigoGetSerializer
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import permissions



def is_curador(user):
    return user.groups.filter(name='curador').exists()

class ApenasLeituraOuCurador(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return is_curador(request.user)

class ArtigoIdView(APIView):
    permission_classes = [ApenasLeituraOuCurador]

    @swagger_auto_schema(
        operation_summary='Dados de um artigo',
        operation_description="Obter informações sobre um artigo específico",
        responses={
            200: ArtigoSerializer(),
            404: 'Artigo não encontrado',
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
        operation_summary='Atualiza artigo', 
        operation_description="Atualizar um artigo existente",
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
        responses={
            200: ArtigoSerializer(),
            400: 'Parâmentros inválidos',
            401: 'Não autorizado',
            404: 'Artigo com id #id não existe',
        },
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
            artigo = Artigo.objects.get(id=id)
            serializer = ArtigoSerializer(artigo, data=request.data)
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
            401: 'Não autorizado',
            404: 'Artigo não encontrado',
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
            artigo = Artigo.objects.get(id=id)
            artigo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Artigo.DoesNotExist:
            return Response({'msg': f'Artigo com id #{id} não existe'},
                            status.HTTP_404_NOT_FOUND)


class ArtigoView(APIView):
    permission_classes = [ApenasLeituraOuCurador]

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
        responses={
            201: ArtigoSerializer(),
            400: 'Parâmetros inválidos',
            401: 'Não autorizado'
        },
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


class AutorIdView(APIView):
    permission_classes = [ApenasLeituraOuCurador]

    @swagger_auto_schema(
        operation_summary='Dados de um autor',
        operation_description="Obter informações sobre um autor específico",
        responses={
            200: ArtigoSerializer(),
            400: 'Parâmetros inválidos',
        },
        manual_parameters=[
            openapi.Parameter('id',in_=openapi.IN_PATH,
                default=5,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='id do autor na URL',
            ),
        ],
    )
    def get(self, request, id):
        try:
            queryset = Autor.objects.get(id=id)
            serializer = AutorSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'msg': f'Autor com id #{id} não existe'},
                            status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary='Atualiza autor', 
        operation_description="Atualizar um autor existente",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nome': openapi.Schema(
                    example='Autor 1', 
                    description='Título do autor',
                    type=openapi.TYPE_STRING,
                    ),
            },
        ),
        responses={
            200: AutorSerializer(),
            400: 'Parâmentros inválidos',
            401: 'Não autorizado',
            404: 'Não encontrado',
        },
        manual_parameters=[
            openapi.Parameter('id',openapi.IN_PATH, default=41, type=openapi.TYPE_INTEGER,
                required=True, description='id do autor na URL',),
        ],
    )
    def put(self, request, id):
        '''
        Atualiza os dados de um autor.
        O ID do autor a ser atualizado vem pela URL.
        '''
        try:
            autor = Autor.objects.get(id=id)
            serializer = AutorSerializer(autor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Autor.DoesNotExist:
            return Response({'msg': f'Autor com id #{id} não existe'},
                            status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary='Deleta autor',
        operation_description="Deletar um autor existente",
        responses={
            204: 'Sem conteúdo',
            401: 'Não autorizado',
            404: 'Autor não encontrado',
        },
        manual_parameters=[
            openapi.Parameter('id',openapi.IN_PATH, default=14,
                type=openapi.TYPE_INTEGER, required=True,
                description='id do autor na URL',),
        ],
    )
    def delete(self, request, id):
        '''
        Deleta um autor.
        O ID do autor a ser deletado vem pela URL.
        '''
        try:
            autor = Autor.objects.get(id=id)
            autor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Autor.DoesNotExist:
            return Response({'msg': f'Autor com id #{id} não existe'},
                            status.HTTP_404_NOT_FOUND)


class AutorView(APIView):
    permission_classes = [ApenasLeituraOuCurador]

    @swagger_auto_schema(
        operation_summary='Criar autor',
        operation_description="Criar um novo autor",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nome': openapi.Schema(
                    example='Autor 1', 
                    description='Nome do autor',
                    type=openapi.TYPE_STRING,
                    ),
            },
            required=['nome'],
        ),
        responses={
            201: AutorSerializer(),
            400: 'Parâmetros inválidos',
            401: 'Não autorizado'
            },
    )
    def post(self, request):
        serializer = AutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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
