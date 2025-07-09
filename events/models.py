from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class TipoEvento(models.TextChoices):
    ASSEMBLEIA = 'assembleia', 'Assembleia'
    REUNIAO = 'reuniao', 'Reunião'
    CURSO = 'curso', 'Curso'
    PALESTRA = 'palestra', 'Palestra'
    CONFRATERNIZACAO = 'confraternizacao', 'Confraternização'
    OUTRO = 'outro', 'Outro'

class StatusEvento(models.TextChoices):
    AGENDADO = 'agendado', 'Agendado'
    EM_ANDAMENTO = 'andamento', 'Em Andamento'
    FINALIZADO = 'finalizado', 'Finalizado'
    CANCELADO = 'cancelado', 'Cancelado'

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField()
    tipo = models.CharField(max_length=20, choices=TipoEvento.choices, default=TipoEvento.REUNIAO)
    status = models.CharField(max_length=20, choices=StatusEvento.choices, default=StatusEvento.AGENDADO)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    local = models.CharField(max_length=200)
    endereco = models.TextField()
    organizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos_organizados')
    capacidade_maxima = models.PositiveIntegerField(null=True, blank=True)
    inscricao_obrigatoria = models.BooleanField(default=False)
    imagem = models.ImageField(upload_to='eventos/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['data_inicio']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'slug': self.slug})
    
    @property
    def vagas_disponivel(self):
        if self.capacidade_maxima:
            return self.capacidade_maxima - self.inscricoes.count()
        return None

class InscricaoEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes')
    participante = models.ForeignKey(User, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    presente = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Inscrição em Evento'
        verbose_name_plural = 'Inscrições em Eventos'
        unique_together = ['evento', 'participante']
        ordering = ['data_inscricao']
    
    def __str__(self):
        return f"{self.participante.get_full_name()} - {self.evento.titulo}"
