from django.contrib import admin

# Register your models here.
from .models import Membro, Contribuicao, TipoContribuicao, StatusContribuicao
@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ('user', 'nome', 'numero_membro', 'tipo_membro', 'status', 'data_nascimento', 'ativo')
    search_fields = ( 'nome', 'cpf')
    list_filter = ('tipo_membro', 'status', 'ativo')
    date_hierarchy = 'data_nascimento'
   # prepopulated_fields = {'numero_membro': ('user__username',)}
    
@admin.register(Contribuicao)
class ContribuicaoAdmin(admin.ModelAdmin):
    list_display = ('membro', 'valor', 'data_pagamento', 'mes_referencia', 'descricao', 'tipo', 'status')
    search_fields = ('descricao',)
    list_filter = ('status',)
    date_hierarchy = 'data_pagamento'

 