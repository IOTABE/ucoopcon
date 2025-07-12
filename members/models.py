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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pessoas')
    pessoa = models.ForeignKey(Pessoas, on_delete=CASCADE, )
    numero_membro = models.CharField(max_length=20, unique=True)
#    nome = models.CharField(max_length=100)
    tipo_membro = models.CharField(max_length=20, choices=TipoMembro.choices, default=TipoMembro.COOPERADO)
    status = models.CharField(max_length=20, choices=StatusMembro.choices, default=StatusMembro.ATIVO)
#    cpf = models.CharField(max_length=14, unique=True)
#    rg = models.CharField(max_length=20)
#    data_nascimento = models.DateField()
#    telefone = models.CharField(max_length=20)
#    endereco = models.TextField()
#    cidade = models.CharField(max_length=100)
#    estado = models.CharField(max_length=2)
#    cep = models.CharField(max_length=9)
    ficha_cadastral_numero = models.IntegerField(blank=True, null=True, help_text='Número da ficha cadastral associada à contribuição')
    term_adesao_numero = models.IntegerField(blank=True, null=True, help_text='Número do termo de adesão associado à contribuição')
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
    

class Parceiros_atividades(models.Model):
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
    atividades = models.ManyToManyField(Parceiros_atividades, related_name='parceiros', blank=True)
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
    forma_pagamento = models.CharField(max_length=20, choices=FormaDePagamento.choices, default=FormaDePagamento.BOLETO)
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
        
    def clean(self):
        if self.valor_promocional and self.valor_promocional >= self.valor_plano:
            raise ValidationError('O valor promocional deve ser menor que o valor do plano.')
        if self.prazo_pagamento < 0:
            raise ValidationError('O prazo de pagamento não pode ser negativo.')
        if self.num_parcelas <= 0:
            raise ValidationError('O número de parcelas deve ser maior que zero.')
        if self.taxa_juros < 0 or self.taxa_desconto < 0:
            raise ValidationError('As taxas de juros e desconto não podem ser negativas.')
        
    def get_total_value(self):
        """
        Calculate the total value of the plan considering the discount and number of installments.
        """
        if self.valor_promocional:
            total_value = self.valor_promocional * self.num_parcelas
        else:
            total_value = self.valor_plano * self.num_parcelas
        
        if self.taxa_juros > 0:
            total_value += (total_value * self.taxa_juros / 100)
        
        if self.taxa_desconto > 0:
            total_value -= (total_value * self.taxa_desconto / 100)
        
        return total_value      
    
    def get_installment_value(self):
        """
        Calculate the value of each installment based on the total value and number of installments.
        """
        total_value = self.get_total_value()
        return total_value / self.num_parcelas if self.num_parcelas > 0 else total_value    
    
    def get_payment_conditions(self):
        """
        Retrieve the payment conditions for the partner.
        """
        return {
            "forma_pagamento": self.forma_pagamento,
            "prazo_pagamento": self.prazo_pagamento,
            "desconto": self.desconto,
            "num_parcelas": self.num_parcelas,
            "taxa_juros": self.taxa_juros,
            "taxa_desconto": self.taxa_desconto,
        }
    
    def get_payment_method_display(self):
        """
        Retrieve the display name for the payment method.
        """
        return dict(FormaDePagamento.choices).get(self.forma_pagamento, self.forma_pagamento)
    
    def get_status_display(self):
        """
        Retrieve the display name for the status.
        """
        return "Ativo" if self.ativo else "Inativo"     
    def get_partner_name(self):
        """
        Retrieve the name of the partner associated with this payment condition.
        """
        return self.parceiro.nome.nome if self.parceiro and self.parceiro.nome else "Parceiro Desconhecido"
    
    def get_partner_contact(self):
        """
        Retrieve the contact information for the partner associated with this payment condition.
        """
        return self.parceiro.contato if self.parceiro and self.parceiro.contato else "Contato Desconhecido" 
    
    def get_partner_email(self):
        """
        Retrieve the email address for the partner associated with this payment condition.
        """
        return self.parceiro.email if self.parceiro and self.parceiro.email else "Email Desconhecido"
    
    def get_partner_phone(self):
        """
        Retrieve the phone number for the partner associated with this payment condition.
        """
        return self.parceiro.telefone if self.parceiro and self.parceiro.telefone else "Telefone Desconhecido"  
    
    def get_partner_website(self):
        """
        Retrieve the website URL for the partner associated with this payment condition.
        """
        return self.parceiro.website if self.parceiro and self.parceiro.website else "Website Desconhecido" 
    
    def get_partner_logo(self):
        """
        Retrieve the logo URL for the partner associated with this payment condition.
        """
        return self.parceiro.logo if self.parceiro and self.parceiro.logo else "Logo Desconhecido"          
    
    def get_partner_activities(self):
        """
        Retrieve the activities for the partner associated with this payment condition.
        """
        return self.parceiro.atividades if self.parceiro and self.parceiro.atividades else "Atividades Desconhecidas"


    def get_partner_address(self):
        """
        Retrieve the address for the partner associated with this payment condition.
        """
        return self.parceiro.endereco if self.parceiro and self.parceiro.endereco else "Endereço Desconhecido"
    
    def get_partner_city(self):
        """
        Retrieve the city for the partner associated with this payment condition.
        """
        return self.parceiro.cidade if self.parceiro and self.parceiro.cidade else "Cidade Desconhecida"

    def get_partner_state(self):
        """
        Retrieve the state for the partner associated with this payment condition.
        """
        return self.parceiro.estado if self.parceiro and self.parceiro.estado else "Estado Desconhecido"    
    
    def get_partner_zip_code(self):
        """
        Retrieve the zip code for the partner associated with this payment condition.
        """
        return self.parceiro.cep if self.parceiro and self.parceiro.cep else "CEP Desconhecido"
    
    
    def get_partner_social_media(self):
        """
        Retrieve the social media links for the partner associated with this payment condition.
        """
        return self.parceiro.redes_sociais if self.parceiro and self.parceiro.redes_sociais else "Redes Sociais Desconhecidas"  
    
    def get_partner_description(self):
        """
        Retrieve the description for the partner associated with this payment condition.
        """
        return self.parceiro.descricao if self.parceiro and self.parceiro.descricao else "Descrição Desconhecida"
    
    def get_partner_type(self):
        """
        Retrieve the type for the partner associated with this payment condition.
        """
        return self.parceiro.tipo if self.parceiro and self.parceiro.tipo else "Tipo Desconhecido"


class parceiros_config(models.Model):
    parceiro = models.ForeignKey(Parceiros, on_delete=models.CASCADE, related_name='configuracoes')
    plano = models.ForeignKey(Planos, on_delete=models.CASCADE, related_name='configuracoes', blank=True, null=True)
    cond_pagamento = models.ForeignKey(ParceiroCondPagamento, on_delete=models.CASCADE, related_name='configuracoes', blank=True, null=True)
    tipo_desc_p = models.CharField(max_length=20, choices=[('percentual', 'Percentual'), ('valor_fixo', 'Valor Fixo')], default='percentual')
    valor_desc_p = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    valor_desc_f = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    desconto_ativo = models.BooleanField(default=False, help_text='Marcar se o desconto está ativo')
    desconto_percentual = models.DecimalField(max_digits=5, decimal_places=2
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração do Parceiro'
        verbose_name_plural = 'Configurações dos Parceiros'
        ordering = ['parceiro', 'plano']
    
    def __str__(self):
        return f"{self.parceiro} - {self.plano}" if self.plano else f"{self.parceiro} - Configuração Padrão"
        

class ParceirosServicos(models.Model):
    parceiro = models.ForeignKey(Parceiros, on_delete=models.CASCADE, related_name='servicos')
    nome_servico = models.CharField(max_length=100)
    descricao_servico = models.TextField(blank=True)
    preco_servico = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    imgservico = models.ImageField(upload_to='parceiros_servicos/', blank=True, null=True)
    categoria_servico = models.CharField(max_length=100, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome_servico} - {self.parceiro}" 
        
    class Meta:
        verbose_name = 'Serviço do Parceiro'
        verbose_name_plural = 'Serviços dos Parceiros'
        ordering = ['parceiro', 'nome_servico']
        
    def get_absolute_url(self):
        return reverse('members:parceiro_servico_detail', kwargs={'pk': self.pk})
        
    def save(self, *args, **kwargs):
        if not self.imgservico:
            self.imgservico = 'parceiros_servicos/default_service.png'  # Default image if none provided
        super().save(*args, **kwargs)   
        
class MembroNegociacao(models.Model):
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, related_name='negociacoes')
    numdocnegcop = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text='Número do documento da negociação')
    formpagto = models.CharField(max_length=20, choices=FormaDePagamento.choices, default=FormaDePagamento.BOLETO)
    isrecebido = models.BooleanField(default=False, help_text='Marcar se a negociação foi recebida')
    dataemissao = models.DateField(default=timezone.now, help_text='Data de emissão da negociação')
    datavencimento = models.DateField(help_text='Data de vencimento da negociação')
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2, help_text='Valor bruto da negociação')
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Valor do desconto aplicado na negociação')
    valor_acrescimo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Valor do acréscimo aplicado na negociação')
    valor_negociado = models.DecimalField(max_digits=10, decimal_places=2, help_text='Valor total negociado')
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2, help_text='Valor líquido da negociação')
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Valor já pago na negociação')
    datapagamento = models.DateField(blank=True, null=True, help_text='Data do pagamento da negociação')
    datacadastro = models.DateTimeField(auto_now_add=True, help_text='Data de cadastro da negociação')
    dataatualizacao = models.DateTimeField(auto_now=True, help_text='Data da última atualização da negociação')
           
    class Meta:
        verbose_name = 'Negociação do Membro'
        verbose_name_plural = 'Negociações dos Membros'
        ordering = ['-data_negociacao']
    
    def __str__(self):
        return f"{self.membro} - {self.parceiro} - R$ {self.valor_negociado} - {self.data_negociacao.strftime('%d/%m/%Y')}"
        
    
class Planos(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    valor_plano = models.DecimalField(max_digits=10, decimal_places=2)
    valor_promocional = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_taxa_boleto = models.BooleanField(default=False, help_text='Marcar se há taxa de boleto')
    taxa_boleto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Valor da taxa de boleto, se aplicável')
    cor_plano = models.CharField(max_length=20, default='blue', help_text='Cor do plano para identificação visual')
    destaque_plano = models.BooleanField(default=False, help_text='Marcar se o plano deve ser destacado na lista')
    img_plano = models.ImageField(upload_to='planos/', blank=True, null=True, help_text='Imagem do plano para identificação visual')
    icon_plano = models.ImageField(upload_to='planos/icons/', blank=True, null=True, help_text='Ícone do plano para identificação visual')    
    ativo = models.BooleanField(default=True)
    apenas_interno = models.BooleanField(default=False, help_text='Marcar se o plano é apenas para uso interno')
    num_solicit_plano = models.IntegerField(blank=True, null=True, help_text='Número de solicitação do plano para controle interno')
    num_cotas = models.IntegerField(default=1, help_text='Número de cotas disponíveis para o plano')
    publico_interno = models.BooleanField(default=False, help_text='Marcar se o plano é apenas para uso interno')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    data_exclusao = models.DateTimeField(null=True, blank=True, help_text='Data de exclusão do plano, se aplicável')
    
    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['nome']
        
    def __str__(self):
        return self.nome
        

class PlanosAnexos(models.Model):
    plano = models.ForeignKey(Planos, on_delete=models.CASCADE, related_name='anexos')
    nome_anexo = models.CharField(max_length=100)
    descricao_anexo = models.TextField(blank=True)
    arquivo_anexo = models.FileField(upload_to='planos/anexos/', blank=True, null=True)
    icon_anexo = models.ImageField(upload_to='planos/anexos/icons/', blank=True, null=True, help_text='Ícone do anexo para identificação visual')
    tipo_arquivo = models.CharField(max_length=20, choices=[('pdf', 'PDF'), ('docx', 'DOCX'), ('xlsx', 'XLSX'), ('jpg', 'JPG'), ('png', 'PNG')], default='pdf')
    tamanho_arquivo = models.PositiveIntegerField(blank=True, null=True, help_text='Tamanho do arquivo em bytes')
    data_upload = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = 'Anexo do Plano'
        verbose_name_plural = 'Anexos dos Planos'
        ordering = ['plano', 'nome_anexo']
    
    def __str__(self):
        return f"{self.plano.nome} - {self.nome_anexo}"
        

class PlanosCondPagto(models.Model):
    plano = models.ForeignKey(Planos, on_delete=models.CASCADE, related_name='cond_pagamentos')
    forma_pagamento = models.CharField(max_length=20, choices=FormaDePagamento.choices, default=FormaDePagamento.BOLETO)
    prazo_pagamento = models.IntegerField(help_text='Prazo em dias para pagamento após a compra')
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Desconto aplicado no valor do plano')
    num_parcelas = models.IntegerField(default=1, help_text='Número de parcelas para pagamento')
    taxa_juros = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Taxa de juros aplicada em caso de parcelamento')
    taxa_desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Taxa de desconto aplicada no valor do plano')
    vlr_parcela = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Valor da parcela do plano')
    vlr_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Valor total do plano considerando parcelas e taxas')
    taxa_juros_parcelas = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Taxa de juros aplicada nas parcelas')
    taxa_desconto_parcelas = models.DecimalField(max_digits=5, decimal_places=
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)  
    
    class Meta:
        verbose_name = 'Condição de Pagamento do Plano'
        verbose_name_plural = 'Condições de Pagamento dos Planos'
        ordering = ['plano', 'forma_pagamento']
    
    def __str__(self):
        return f"{self.plano.nome} - {self.forma_pagamento}"
        
        
class PlanosPublicos(models.Model):
    plano = models.ForeignKey(Planos, on_delete=models.CASCADE, related_name='publicos')
    nome_publico = models.CharField(max_length=100, unique=True)
    descricao_publica = models.TextField(blank=True)
    valor_publico = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Plano Público'
        verbose_name_plural = 'Planos Públicos'
        ordering = ['nome_publico']
    
    def __str__(self):
        return self.nome_publico
        
                    