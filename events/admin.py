from django.contrib import admin
from .models import Evento as Event, InscricaoEvento as Inscription

 
@admin.register(Event)
class EventAdmin(admin.ModelAdmin): 
    list_display = ('titulo', 'slug', 'descricao', 'tipo', 'status', 'data_inicio', 'data_fim', 'local', 'endereco', 'organizador', 'capacidade_maxima', 'inscricao_obrigatoria', 'imagem')
    list_filter = ('tipo', 'status', 'data_inicio', 'data_fim', 'organizador')
    search_fields = ('titulo', 'descricao')
    list_filter = ('tipo', 'status', )
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'data_inicio'

@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('evento', 'participante', 'data_inscricao', 'presente')
    search_fields = ('evento__titulo', 'participante__username')
    list_filter = ('presente',)
    date_hierarchy = 'data_inscricao'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('evento', 'participante')

    def participante(self, obj):
        return obj.participante.username if obj.participante else 'N/A'

    participante.admin_order_field = 'participante__username'
    participante.short_description = 'Participant Username'

    def evento(self, obj):
        return obj.evento.titulo if obj.evento else 'N/A'

    evento.admin_order_field = 'evento__titulo'
    evento.short_description = 'Event Title'

    def data_inscricao(self, obj):
        return obj.data_inscricao.strftime('%Y-%m-%d %H:%M:%S')

    data_inscricao.admin_order_field = 'data_inscricao'
    data_inscricao.short_description = 'Registration Date'

    def presente(self, obj):
        return 'Yes' if obj.presente else 'No'

    presente.boolean = True
    presente.admin_order_field = 'presente'
    presente.short_description = 'Present'

    def has_add_permission(self, request, obj=None):
        return False  # Disable adding inscriptions through the admin interface

    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting inscriptions through the admin interface

    def has_change_permission(self, request, obj=None):
        return False    