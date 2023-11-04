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
    

class Artigo(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, 
                            help_text='Insira o título do artigo',
                            verbose_name='Título do artigo*')
    ano_publicacao = models.CharField(max_length=4, 
                                      help_text='Insira o ano de publicação' +
                                       ' do artigo',
                                      verbose_name='Ano de publicação*',
                        validators=[MinLengthValidator(4,
                            'Campo precisa ter 4 dígitos.')])
    autores = models.ManyToManyField(Autor, help_text="Para selecionar mais" +
                                     " de um autor, segure" +
                                     " a tecla Ctrl ao clicar.",
                                     verbose_name="Autores*")
    link = models.URLField(blank=True,
            verbose_name='Link',
            help_text= 'Insira o link para o artigo (Opcional)')

    class Meta:
        ordering = ["nome"]
        
    def __str__(self):
        return self.nome

