from django.conf import empty
from django.db import models
from django.core.validators import MinLengthValidator


class Autor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, help_text='Insira o nome do autor',
                            verbose_name='Nome do autor*')
    
    class Meta:
        ordering = ["nome"]
        
    def __str__(self):
        return self.nome

    @property
    def n_artigos(self):
        return self.artigo_set.count()
    

class Artigo(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, 
                            verbose_name='Título do artigo')
    ano_publicacao = models.CharField(
            max_length=4,
            verbose_name='Ano de publicação',
            validators=[MinLengthValidator(4, 'Campo precisa ter 4 dígitos.')]
            )
    autores = models.ManyToManyField(Autor, verbose_name="Autores", blank=True)
    link = models.URLField(blank=True, verbose_name='Link')

    class Meta:
        ordering = ["nome"]
        
    def __str__(self):
        return self.nome
