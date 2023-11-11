"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend import views
from django.urls.conf import include
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy

from rest_framework import routers
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as yasg_schema_view
from drf_yasg import openapi

app_name = "backend"

schema_view = yasg_schema_view(
    openapi.Info(
        title="API de Exemplo",
        default_version='v1',
        description="Descrição da API de exemplo",
        contact=openapi.Contact(email="meslin@puc-rio.br"),
        license=openapi.License(name='GNU GPLv3'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('docs/', include_docs_urls(title='Documentação da API')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/', include(routers.DefaultRouter().urls)),
    path('openapi', get_schema_view(
        title="API para Artigos",
        description="API para obter dados dos artigos",),
        name='openapi-schema'
    ),
    
    path('', views.home, name='home-page'),
    path('admin/', admin.site.urls),
    path('artigos/', include('artigos.urls')),
    path('accounts/', include('accounts.urls')),
    path('seguranca/', views.homeSec, name='sec-home'),
    path('seguranca/registro/', views.registro, name='sec-registro'),
    
    path('seguranca/login/', 
         LoginView.as_view(template_name='seguranca/login.html',
                           extra_context={
                               'titulo': 'Login',
                                'tituloPagina': 'Login de Usuário',
                                'textoBotao': 'Login',}
                           ), 
         name='sec-login'),
    
    path('logout/',
         LogoutView.as_view(next_page=reverse_lazy('sec-home'),),
         name='sec-logout'),
    
    path('seguranca/troca_senha/',
        PasswordChangeView.as_view(
            template_name='seguranca/usuario.html',
            extra_context={
                'titulo': 'Troca Senha',
                'tituloPagina': 'Troca de Senha de Usuário',
                'textoBotao': 'Trocar Senha',
            },
            success_url=reverse_lazy('sec-password_change_done'),
        ), 
        name='sec-password_change'),
    
    path('seguranca/troca_senha_finalizada/',
        PasswordChangeDoneView.as_view(
            template_name='seguranca/password_change_done.html',
        ), name='sec-password_change_done'),

    path('seguranca/termina_registro/<int:pk>/',
        UpdateView.as_view(
            template_name='seguranca/usuario.html',
            extra_context={
                'titulo': 'Termina Registro',
                'tituloPagina': 'Termina Registro de Usuário',
                'textoBotao': 'Atualiza',
            },
            success_url=reverse_lazy('sec-home'),
            model=User,
            fields=[
                'first_name',
                'last_name',
                'email',
            ],
        ), name='sec-user_confirm_data'),

        path('seguranca/password_reset/', 
            PasswordResetView.as_view(
                template_name='seguranca/usuario.html',
                extra_context={
                    'titulo': 'Recuperação de Senha',
                    'tituloPagina': 'Recuperação de Senha de Usuário',
                    'textoBotao': 'Envia e-mail',
                },
                success_url=reverse_lazy('sec-password_reset_done'),
                html_email_template_name='seguranca/password_reset_email.html',
                subject_template_name='seguranca/password_reset_subject.txt',
                from_email='gbanaggia@gmail.com',
            ), name='password_reset'),

        path('seguranca/password_reset_done/', 
            PasswordResetDoneView.as_view(
                template_name='seguranca/password_reset_done.html',
            ), name='sec-password_reset_done'),

        path('seguranca/password_reset_confirm/<uidb64>/<token>/',
            PasswordResetConfirmView.as_view(
                template_name='seguranca/password_reset_confirm.html',
                success_url=reverse_lazy('sec-password_reset_complete'),
            ), name='password_reset_confirm'),

        path('seguranca/password_reset_complete/', 
            PasswordResetCompleteView.as_view(
                template_name='seguranca/password_reset_complete.html'
            ), name='sec-password_reset_complete'),
]
