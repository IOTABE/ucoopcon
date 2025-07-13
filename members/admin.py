from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Membro, Contribuicao, TipoContribuicao, StatusContribuicao

@admin.register(Membro)
class MembroAdmin(ModelAdmin):
    list_display = ('user', 'nome', 'numero_membro', 'tipo_membro', 'status', 'data_nascimento', 'ativo')
    search_fields = ('pessoa__nome', 'pessoa__cpf')
    list_filter = ('tipo_membro', 'status', 'ativo')
    date_hierarchy = 'pessoa__data_nascimento'

    def nome(self, obj):
        return obj.pessoa.nome
    nome.admin_order_field = 'pessoa__nome'
    nome.short_description = 'Nome'

    def data_nascimento(self, obj):
        return obj.pessoa.data_nascimento
    data_nascimento.admin_order_field = 'pessoa__data_nascimento'
    data_nascimento.short_description = 'Data de Nascimento'

@admin.register(Contribuicao)
class ContribuicaoAdmin(ModelAdmin):
    list_display = ('membro', 'valor', 'data_pagamento', 'mes_referencia', 'descricao', 'tipo', 'status')
    search_fields = ('descricao',)
    list_filter = ('status',)
    date_hierarchy = 'data_pagamento'

