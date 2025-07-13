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
    

class FormaDePagamento(models.TextChoices):
    BOLETO = 'boleto', 'Boleto'
    CARTAO_CREDITO = 'cartao_credito', 'Cartão de Crédito'
    TRANSFERENCIA = 'transferencia', 'Transferência'
    DINHEIRO = 'dinheiro', 'Dinheiro'
    PIX = 'pix', 'PIX'
    CHEQUEAVISTA = 'chequeavista', 'Cheque à Vista'
    CHEQUEPARCELADO = 'chequeparcelado', 'Cheque Parcelado'
    DEPOSITO = 'deposito', 'Depósito'
    CONSIGNADO = 'consignado', 'Consignado'
    VALEALIMENTACAO = 'valealimentacao', 'Vale Alimentação'
    VALETRANSPORTE = 'valetransporte', 'Vale Transporte'
    TRANSFERENCIABANCARIA = 'transferenciabancaria', 'Transferência Bancária'
    CREDIARIOPROPRIO = 'crediariopropio', 'Crediário Próprio'
    CARTAO_DEBITO = 'cartao_debito', 'Cartão de Débito'
    
    
class Profissoes(models.Model):
    nome_profissao = models.CharField(max_length=100, unique=True)
    requer_registro = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Profissão'
        verbose_name_plural = 'Profissões'
        ordering = ['nome_profissao']

    def __str__(self):
        return self.nome_profissao


class Ufs(models.Model):
    sigla = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=100)
    dt_cad = models.DateTimeField(auto_now_add=True)
    dt_update = models.DateTimeField(auto_now=True)
    dt_delete = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'UF'
        verbose_name_plural = 'UFs'
        ordering = ['sigla']

    def __str__(self):
        return self.sigla

class TipoPessoa(models.TextChoices):
    FISICA = 'fisica', 'Pessoa Física'
    JURIDICA = 'juridica', 'Pessoa Jurídica'
    
    
class PessoasRelacoes(models.Model):
    descricao = models.CharField(max_length=100, unique=True)
    grau_parentesco = models.CharField(max_length=50, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    

class Pessoas(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TipoPessoa.choices, default=TipoPessoa.FISICA)
    is_dependente_pessoa = models.BooleanField(default=False, help_text='Marcar se é dependente de outra pessoa')
    profissao = models.ForeignKey(Profissoes, on_delete=models.CASCADE, related_name='pessoas', blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=10, choices=[('masculino', 'Masculino'), ('feminino', 'Feminino')], blank=True, null=True)
    rg = models.CharField(max_length=20, unique=True, blank=True, null=True)
    orgao_expedidor_rg = models.CharField(max_length=20, blank=True, null=True)
    data_expedicao_rg = models.DateField(blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    cnpj = models.CharField(max_length=18, unique=True, blank=True, null=True)
    razao_social = models.CharField(max_length=200, blank=True, null=True)
    nome_fantasia = models.CharField(max_length=200, blank=True, null=True)
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True)
    inscricao_municipal = models.CharField(max_length=20, blank=True, null=True)
    ie_substituta = models.CharField(max_length=20, blank=True, null=True)
    ie_st = models.CharField(max_length=20, blank=True, null=True)
    ie_municipal = models.CharField(max_length=20, blank=True, null=True)
    ie_estadual = models.CharField(max_length=20, blank=True, null=True)
    ie_federal = models.CharField(max_length=20, blank=True, null=True)
    ie_matriz_filial = models.CharField(max_length=20, blank=True, null=True)
    ie_suframa = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    estado_civil = models.CharField(max_length=20, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('divorciado', 'Divorciado'), ('viuvo', 'Viúvo')], blank=True, null=True)
    nacionalidade = models.CharField(max_length=50, blank=True, null=True)
    naturalidade = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    telefone_comercial = models.CharField(max_length=20, blank=True, null=True)
    telefone_celular = models.CharField(max_length=20, blank=True, null=True)
    telefone_residencial = models.CharField(max_length=20, blank=True, null=True)
    telefone_outro = models.CharField(max_length=20, blank=True, null=True)
    cidade = models.ForeignKey('Cidades', on_delete=models.CASCADE, related_name='pessoas')
    estado = models.ForeignKey(Ufs, on_delete=models.CASCADE, related_name='pessoas')
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    foto = models.ImageField(upload_to='pessoas/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    status_cadastro = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('aprovado', 'Aprovado'), ('rejeitado', 'Rejeitado')], default='pendente')
    status_financeiro = models.CharField(max_length=20, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo')
    cod_indicacao_pessoa = models.CharField(max_length=20, unique=True, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    data_exclusao = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('members:detail', kwargs={'pk': self.pk})
    data_cadastro = models.DateTimeField(auto_now_add=True)    
    
    
class Cidades(models.Model):
    nome = models.CharField(max_length=100)
    uf = models.ForeignKey(Ufs, on_delete=models.CASCADE, related_name='cidades')
    cep_geral_cidade = models.CharField(max_length=9, blank=True, null=True)
    cod_ibg_cidade = models.CharField(max_length=10, unique=True, blank=True, null=True)
    dt_cad = models.DateTimeField(auto_now_add=True)
    dt_update = models.DateTimeField(auto_now=True)
    dt_delete = models.DateTimeField(null=True, blank=True)    

class Membro(models.Model):
    pessoa = models.OneToOneField('Pessoas', on_delete=models.CASCADE, related_name='membro',null=True )
    numero_membro = models.CharField(max_length=20, unique=True)
    plano = models.ForeignKey('Planos', on_delete=models.PROTECT, default=None)
    parcelas = models.PositiveIntegerField(default=1)
    tipo_membro = models.CharField(max_length=20, choices=TipoMembro.choices, default=TipoMembro.COOPERADO)
    status = models.CharField(max_length=20, choices=StatusMembro.choices, default=StatusMembro.ATIVO)
    ficha_cadastral_numero = models.IntegerField(blank=True, null=True, help_text='Número da ficha cadastral associada à contribuição')
    term_adesao_numero = models.IntegerField(blank=True, null=True, help_text='Número do termo de adesão associado à contribuição')
    data_adesao = models.DateField(default=timezone.now)
    foto = models.ImageField(upload_to='membros/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'
        ordering = ['pessoa__nome']
    
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
    

class ParceirosAtividades(models.Model):
    nome_ativ = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    icon_ativ = models.ImageField(upload_to='parceiros_atividades/', blank=True, null=True)
    cod_ativ = models.CharField(max_length=20, unique=True, blank=True, null=True)  
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True) 
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Atividade do Parceiro'
        verbose_name_plural = 'Atividades dos Parceiros'
        ordering = ['nome_ativ']
        
    def __str__(self):
        return self.nome_ativ
    
    
   
class Parceiros(models.Model):
    nome = models.ForeignKey(Pessoas, on_delete=models.CASCADE, related_name='parceiros')
    atividades = models.ManyToManyField(ParceirosAtividades, related_name='parceiros', blank=True)
    tipo_parceiro = models.CharField(max_length=20, choices=[('fornecedor', 'Fornecedor'), ('cliente', 'Cliente'), ('parceiro', 'Parceiro')], default='parceiro')
    contato = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    descricao = models.TextField(blank=True)
    site = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='parceiros/', blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Parceiro'
        verbose_name_plural = 'Parceiros'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('members:parceiro_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.logo:
            self.logo = 'parceiros/default_logo.png'  # Default logo if none provided


class Planos(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    valor_plano = models.DecimalField(max_digits=10, decimal_places=2)
    valor_promocional = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)    


class ParceiroCondPagamento(models.Model):
    parceiro = models.ForeignKey(Parceiros, on_delete=models.CASCADE, related_name='cond_pagamentos')
    forma_pagamento = models.CharField(max_length=25, choices=FormaDePagamento.choices, default=FormaDePagamento.BOLETO)
    prazo_pagamento = models.IntegerField(help_text='Prazo em dias para pagamento após a compra')
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Desconto aplicado no valor do plano')
    num_parcelas = models.IntegerField(default=1, help_text='Número de parcelas para pagamento')
    taxa_juros = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Taxa de juros aplicada em caso de parcelamento')
    taxa_desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Taxa de desconto aplicada no valor do plano')
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)  
    
    class Meta:
        verbose_name = 'Condição de Pagamento do Parceiro'
        verbose_name_plural = 'Condições de Pagamento dos Parceiros'
        ordering = ['parceiro', 'forma_pagamento']
    
    def __str__(self):
        return f"{self.parceiro} - {self.forma_pagamento}"    

    def get_absolute_url(self):
        return reverse('members:cond_pagamento_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.ativo:
            self.data_atualizacao = timezone.now()
        super().save(*args, **kwargs)

