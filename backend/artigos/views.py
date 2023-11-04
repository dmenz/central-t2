from rest_framework.views import APIView
from artigos.models import Autor, Artigo
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
    def get(self, request, id_arg):
        pass

    @swagger_auto_schema()
    def put(self, request, id_arg):
        pass


class ArtigosView(APIView):
    
    @swagger_auto_schema()
    def get(self, request):
        pass

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
    @swagger_auto_schema()
    def get(self, request):
        pass
