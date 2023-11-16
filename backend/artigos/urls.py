from django.urls import path
from artigos import views

app_name = 'artigos'

urlpatterns = [
    path('artigo/', views.ArtigoView.as_view()),
    path('artigo/<id>/', views.ArtigoIdView.as_view()),
    path('artigos/', views.ArtigosView.as_view()),

    path('autor/', views.AutorView.as_view()),
    path('autor/<id>/', views.AutorIdView.as_view()),
    path('autores/', views.AutoresView.as_view()),
]
