from django.shortcuts import render

# Create your views here.

from contatos.models import Pessoa
from django.views.generic.base import View

from contatos.forms import ContatoModel2Form
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy

from django.shortcuts import get_object_or_404


class ContatoListView(View):
    def get(self, request, *args, **kwargs):
        pessoas = Pessoa.objects.all()
        contexto = { 'pessoas': pessoas, }
        return render(
            request,
            'contatos/listaContatos.html',
            contexto)


class ContatoCreateView(View):
    def get(self, request, *args, **kwargs):
        contexto = { 'formulario': ContatoModel2Form, 
                     'tituloPagina': 'Cria um Contato',
                     'nomeBotao' : "Cria contato",
                    }
        return render(request, "contatos/formContato.html", contexto)

    def post(self, request, *args, **kwargs):
        formulario = ContatoModel2Form(request.POST)
        if formulario.is_valid():
            contato = formulario.save()
            contato.save() # salva efetivamente no banco de dados
            return HttpResponseRedirect(reverse_lazy("contatos:lista-contatos"))


class ContatoUpdateView(View):
    def get(self, request, pk, *args, **kwargs):
        pessoa = Pessoa.objects.get(pk=pk)
        formulario = ContatoModel2Form(instance=pessoa)
        context = {'formulario': formulario, 
                   'tituloPagina': 'Atualiza um Contato',
                   'nomeBotao' : "Atualiza contato", 
                   }
        return render(request, 'contatos/formContato.html', context)

    def post(self, request, pk, *args, **kwargs):
        pessoa = get_object_or_404(Pessoa, pk=pk)
        formulario = ContatoModel2Form(request.POST, instance=pessoa)
        if formulario.is_valid():
            pessoa = formulario.save() # cria uma pessoa com os dados do formulário
            pessoa.save() # salva uma pessoa no banco de dados
            return HttpResponseRedirect(reverse_lazy("contatos:lista-contatos"))
        else:
            contexto = {'formulario': formulario, 'tituloPagina': 'Atualiza um Contato', }
            return render(request, 'contatos/formContato.html', contexto)


class ContatoDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        pessoa = Pessoa.objects.get(pk=pk)
        contexto = { 'pessoa': pessoa, }
        return render(request, 'contatos/apagaContato.html', contexto)

    def post(self, request, pk, *args, **kwargs):
        pessoa = Pessoa.objects.get(pk=pk)
        pessoa.delete()
        return HttpResponseRedirect(reverse_lazy("contatos:lista-contatos"))
