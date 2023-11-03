#from django.shortcuts import render

from carros.serializers import MTCarsSerializer
from rest_framework.views import APIView
from carros.models import MTCars
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
class CarView(APIView):

    @swagger_auto_schema(
        operation_summary='Criar carro',
        operation_description="Criar um novo carro",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(default='Honda HRV 2021', description='Modelo do carro', type=openapi.TYPE_STRING),
                'mpg': openapi.Schema(default=24.85, description='Milhas por galão', type=openapi.TYPE_NUMBER),
                'cyl': openapi.Schema(default=4, description='Quantidade de cilindros', type=openapi.TYPE_INTEGER),
                'disp': openapi.Schema(default=1.8, description='Volume do motor', type=openapi.TYPE_NUMBER),
                'hp': openapi.Schema(default=140, description='Potência em HP', type=openapi.TYPE_INTEGER),
                'drat': openapi.Schema(default=3.0, description='Relação do eixo traseiro', type=openapi.TYPE_NUMBER),
                'wt': openapi.Schema(default=2.87686, description='Peso em 1000 libras', type=openapi.TYPE_NUMBER),
                'qsec': openapi.Schema(default=11.88, description='Tempo para percorrer 1/4 milha', type=openapi.TYPE_NUMBER),
                'vs': openapi.Schema(default=0, description='Motor em V ou em linha (straight) (0=v, 1=s)', type=openapi.TYPE_INTEGER),
                'am': openapi.Schema(default=0, description='Transmissão (0=automática, 1=manual)', type=openapi.TYPE_INTEGER),
                'gear': openapi.Schema(default=7, description='Número de marchas para frente', type=openapi.TYPE_INTEGER),
                'carb': openapi.Schema(default=0, description='Número de carburadores', type=openapi.TYPE_INTEGER),
            },
        ),
        responses={201: MTCarsSerializer(), 400: 'Dados errados',},
    )
    def post(self, request):
        '''
        Cria um carro
        '''
        serializer = MTCarsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # uma boa prática é retornar o próprio objeto a
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary='Dados de um carro',
        operation_description="Obter informações sobre um carro específico",
        responses={
            200: MTCarsSerializer(),
            400: 'Mensagem de erro',
        },
        manual_parameters=[
            openapi.Parameter('id_arg',openapi.IN_PATH,
                default=5,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='id do carro na URL',
            ),
        ],
    )
    def get(self, request, id_arg):
        '''
        Retorna um carro pelo seu ID
        O ID deve ser enviado pela URL
        '''
        queryset = self.singleCar(id_arg)
        if queryset:
            serializer = MTCarsSerializer(queryset)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            # response for IDs that is not an existing car
            return Response({'msg': f'Carro com id #{id_arg} não existe'},
                             status.HTTP_400_BAD_REQUEST)
    
    def singleCar(self, id_arg):
        try:
            queryset = MTCars.objects.get(id=id_arg)
            return queryset
        except MTCars.DoesNotExist: # id não existe
            return None

    @swagger_auto_schema(
        operation_summary='Atualiza carro', operation_description="Atualizar um carro existente",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(default='Honda HRV 2021', description='Modelo do carro', type=openapi.TYPE_STRING),
                'mpg': openapi.Schema(default=24.85, description='Milhas por galão', type=openapi.TYPE_NUMBER),
                'cyl': openapi.Schema(default=4, description='Quantidade de cilindros', type=openapi.TYPE_INTEGER),
                'disp': openapi.Schema(default=1.8, description='Volume do motor', type=openapi.TYPE_NUMBER),
                'hp': openapi.Schema(default=140, description='Potência em HP', type=openapi.TYPE_INTEGER),
                'drat': openapi.Schema(default=3.0, description='Relação do eixo traseiro', type=openapi.TYPE_NUMBER),
                'wt': openapi.Schema(default=2.87686, description='Peso em 1000 libras', type=openapi.TYPE_NUMBER),
                'qsec': openapi.Schema(default=11.88, description='Tempo para percorrer 1/4 milha', type=openapi.TYPE_NUMBER),
                'vs': openapi.Schema(default=0, description='Motor em V ou em linha (straight) (0=v, 1=s)', type=openapi.TYPE_INTEGER),
                'am': openapi.Schema(default=0, description='Transmissão (0=automática, 1=manual)', type=openapi.TYPE_INTEGER),
                'gear': openapi.Schema(default=7, description='Número de marchas para frente', type=openapi.TYPE_INTEGER),
                'carb': openapi.Schema(default=0, description='Número de carburadores', type=openapi.TYPE_INTEGER),
            },
        ),
        responses={200: MTCarsSerializer(), 400: MTCarsSerializer(), },
        manual_parameters=[
            openapi.Parameter('id_arg',openapi.IN_PATH, default=41, type=openapi.TYPE_INTEGER,
                required=True, description='id do carro na URL',),
        ],
    )
    def put(self, request, id_arg):
        '''
        Atualiza os dados de um carro.
        O ID do carro a ser atualizado vem pela URL.'''
        carro = self.singleCar(id_arg)
        serializer = MTCarsSerializer(carro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CarsView(APIView):
    
    @swagger_auto_schema(
        operation_summary='Lista todos os carros',
        operation_description="Obter informações sobre todos os carros",
        request_body=None, # opcional
        responses={200: MTCarsSerializer()}
    )
    def get(self, request):
        queryset = MTCars.objects.all().order_by('name')
        # importante informar que o queryset terá mais
        # de 1 resultado usando many=True
        serializer = MTCarsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(('DELETE',))
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(
        operation_description='Remove um carro',
        request_body=MTCarsSerializer,
        responses={
            204: MTCarsSerializer(),
            404: None,
        },
    )
    def delete(self, request):
        id_erro = ""
        erro = False
        for id in request.data:
            carro = MTCars.objects.get(id=id)
            if carro:
                carro.delete()
            else:
                id_erro += str(id) + ' '
                erro = True
        if erro:
           return Response({'error': f'Itens [{id_erro}] não encontrados'},
                           status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
