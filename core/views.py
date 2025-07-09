from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum, Count
from django.utils import timezone

# Importar os models condicionalmente para evitar erros se os apps não existirem
try:
    from news.models import Noticia, StatusNoticia
except ImportError:
    Noticia = None
    StatusNoticia = None

try:
    from events.models import Evento, StatusEvento
except ImportError:
    Evento = None
    StatusEvento = None

try:
    from members.models import Membro, Contribuicao
except ImportError:
    Membro = None
    Contribuicao = None

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas básicas
        if Membro:
            context['total_membros'] = Membro.objects.filter(ativo=True).count()
        else:
            context['total_membros'] = 0
            
        if Contribuicao:
            total_contrib = Contribuicao.objects.aggregate(total=Sum('valor'))['total']
            context['total_contribuicoes'] = total_contrib or 0
        else:
            context['total_contribuicoes'] = 0
        
        # Notícias em destaque
        if Noticia and StatusNoticia:
            context['noticias_destaque'] = Noticia.objects.filter(
                status=StatusNoticia.PUBLICADA,
                destaque=True
            )[:3]
            context['total_noticias'] = Noticia.objects.filter(
                status=StatusNoticia.PUBLICADA
            ).count()
        else:
            context['noticias_destaque'] = []
            context['total_noticias'] = 0
        
        # Próximos eventos
        if Evento and StatusEvento:
            context['proximos_eventos'] = Evento.objects.filter(
                status=StatusEvento.AGENDADO,
                data_inicio__gte=timezone.now()
            )[:3]
            context['total_eventos'] = Evento.objects.filter(
                status=StatusEvento.FINALIZADO
            ).count()
        else:
            context['proximos_eventos'] = []
            context['total_eventos'] = 0
        
        return context

class SobreView(TemplateView):
    template_name = 'core/sobre.html'

class ContatoView(TemplateView):
    template_name = 'core/contato.html'

class ServicosView(TemplateView):
    template_name = 'core/servicos.html'  # Mudança aqui: de 'servicos.html' para 'servico.html'
