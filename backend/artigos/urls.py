from django.urls import path
from artigos import views

app_name = 'artigos'

urlpatterns = [
    path('artigo/', views.ArtigoView.as_view()),
    path('artigos/', views.ArtigosView.as_view()),
]
