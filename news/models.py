from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    cor = models.CharField(max_length=7, default='#007bff', help_text='Cor em hexadecimal')
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class StatusNoticia(models.TextChoices):
    RASCUNHO = 'rascunho', 'Rascunho'
    PUBLICADA = 'publicada', 'Publicada'
    ARQUIVADA = 'arquivada', 'Arquivada'

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    resumo = models.TextField(max_length=300, help_text='Resumo da notícia (máx. 300 caracteres)')
    conteudo = models.TextField()
    imagem_destaque = models.ImageField(upload_to='noticias/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusNoticia.choices, default=StatusNoticia.RASCUNHO)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_publicacao = models.DateTimeField(null=True, blank=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    destaque = models.BooleanField(default=False, help_text='Marcar como notícia de destaque')
    visualizacoes = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'
        ordering = ['-data_publicacao', '-data_criacao']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.status == StatusNoticia.PUBLICADA and not self.data_publicacao:
            self.data_publicacao = timezone.now()
        super().save(*args, **kwargs)
