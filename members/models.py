from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TipoMembro(models.TextChoices):
    COOPERADO = 'cooperado', 'Cooperado'
    FUNCIONARIO = 'funcionario', 'Funcionário'
    CONSELHEIRO = 'conselheiro', 'Conselheiro'
    PRESIDENTE = 'presidente', 'Presidente'
    

class StatusMembro(models.TextChoices):
    ATIVO = 'ativo', 'Ativo'
    INATIVO = 'inativo', 'Inativo'
    SUSPENSO = 'suspenso', 'Suspenso'

class Membro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_membro = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    tipo_membro = models.CharField(max_length=20, choices=TipoMembro.choices, default=TipoMembro.COOPERADO)
    status = models.CharField(max_length=20, choices=StatusMembro.choices, default=StatusMembro.ATIVO)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    data_adesao = models.DateField(default=timezone.now)
    foto = models.ImageField(upload_to='membros/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'
        ordering = ['user__first_name', 'user__last_name']
    
    def __str__(self):
        return f"{self.numero_membro} - {self.user.get_full_name()}"

class TipoContribuicao(models.TextChoices):
    MENSAL = 'mensal', 'Mensal'
    ANUAL = 'anual', 'Anual'
    EXTRA = 'extra', 'Extra'

class StatusContribuicao(models.TextChoices):
    PAGO = 'pago', 'Pago'
    PENDENTE = 'pendente', 'Pendente'
    ATRASADO = 'atrasado', 'Atrasado'
    CANCELADO = 'cancelado', 'Cancelado'

class Contribuicao(models.Model):
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, related_name='contribuicoes')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField()
    mes_referencia = models.DateField()
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TipoContribuicao.choices, default=TipoContribuicao.MENSAL)
    status = models.CharField(max_length=20, choices=StatusContribuicao.choices, default=StatusContribuicao.PAGO)
    comprovante = models.FileField(upload_to='comprovantes/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        verbose_name = 'Contribuição'
        verbose_name_plural = 'Contribuições'
        ordering = ['-data_pagamento']
    
    def __str__(self):
        return f"{self.membro} - R$ {self.valor} - {self.mes_referencia.strftime('%m/%Y')}"