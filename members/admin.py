from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Membro, Contribuicao, TipoContribuicao, StatusContribuicao

@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ('numero_membro', 'pessoa', 'plano', 'parcelas', 'ficha_cadastro_link', 'termo_adesao_link')
    readonly_fields = ('ficha_cadastro_link', 'termo_adesao_link')

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
class ContribuicaoAdmin(admin.ModelAdmin):
    list_display = ('membro', 'valor', 'data_pagamento', 'mes_referencia', 'descricao', 'tipo', 'status')
    search_fields = ('descricao',)
    list_filter = ('status',)
    date_hierarchy = 'data_pagamento'

