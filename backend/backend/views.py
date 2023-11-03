from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def home(request):
    return render(request, 'backend/home.html')


def homeSec(request):
    return render(request, "seguranca/homeSec.html")


def registro(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('sec-home')
    else:
        formulario = UserCreationForm()
    context = {'form': formulario, 
               'titulo': 'Registro',
               'tituloPagina': 'Registro de Usuário',
               'textoBotao': 'Registro',}
    return render(request, 'seguranca/usuario.html', context)
