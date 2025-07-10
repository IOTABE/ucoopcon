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


class Faq_classes(models.TextChoices):
    COOPERADOS = 'cooperados', 'Cooperados'
    PARCEIROS = 'parceiros', 'Parceiros'
    FORNECEDORES = 'fornecedores', 'Fornecedores'
    


class Conteudos(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    classe_faq = models.CharField(max_length=20, choices=Faq_classes.choices, default=Faq_classes.COOPERADOS)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to='conteudos/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Conteúdo'
        verbose_name_plural = 'Conteúdos'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('news:content_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.titulo.lower().replace(' ', '-')
        super().save(*args, **kwargs)       

        
class faq(models.Model):
    pergunta = models.CharField(max_length=200)
    resposta = models.TextField()
    isativo = models.BooleanField(default=True, help_text='Marcar como FAQ ativo')
    titulo = models.CharField(max_length=200, blank=True, null=True)
    ordem = models.PositiveIntegerField(default=0, help_text='Ordem de exibição')
    num_views = models.PositiveIntegerField(default=0, help_text='Número de visualizações')
    num_likes = models.PositiveIntegerField(default=0, help_text='Número de curtidas')
    num_unlikes = models.PositiveIntegerField(default=0, help_text='Número de descurtidas')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['ordem', '-data_criacao']
    
    def __str__(self):
        return self.pergunta
    
    def get_absolute_url(self):
        return reverse('news:faq_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.titulo:
            self.titulo = self.pergunta
        super().save(*args, **kwargs)
    
    