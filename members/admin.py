from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html

# Register your models here.
from .models import Membro, Contribuicao, TipoContribuicao, StatusContribuicao

@admin.register(Membro)
class MembroAdmin(ModelAdmin):
    list_display = ('nome', 'numero_membro', 'plano', 'parcelas', 'ficha_cadastro_link', 'termo_adesao_link')
    readonly_fields = ('ficha_cadastro_link', 'termo_adesao_link')
    search_fields = ('pessoa__nome', 'pessoa__cpf')
    list_filter = ('tipo_membro', 'status', 'ativo')
   
    def nome(self, obj):
        return obj.pessoa.nome if obj.pessoa else 'N/A'

    nome.admin_order_field = 'pessoa__nome'
    nome.short_description = 'Nome'
    
    def data_nascimento(self, obj):
        return obj.pessoa.data_nascimento.strftime('%Y-%m-%d') if obj.pessoa and obj.pessoa.data_nascimento else 'N/A'
    
    data_nascimento.admin_order_field = 'pessoa__data_nascimento'
    data_nascimento.short_description = 'Data de Nascimento'
    
    
    def ficha_cadastro_link(self, obj):
        if obj.pk:
            url = f"/membros/membro/{obj.pk}/ficha-cadastro/"
            return format_html('<a href="{}" target="_blank">Ficha de Cadastro</a>', url)
        return "-"
    ficha_cadastro_link.short_description = "Ficha de Cadastro"

    def termo_adesao_link(self, obj):
        if obj.pk:
            url = f"/membros/membro/{obj.pk}/termo-adesao/"
            return format_html('<a href="{}" target="_blank">Termo de Adesão</a>', url)
        return "-"
    termo_adesao_link.short_description = "Termo de Adesão"

@admin.register(Contribuicao)
class ContribuicaoAdmin(ModelAdmin):
    list_display = ('membro', 'valor', 'data_pagamento', 'mes_referencia', 'descricao', 'tipo', 'status')
    search_fields = ('descricao',)
    list_filter = ('status',)
    date_hierarchy = 'data_pagamento'

