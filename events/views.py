from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from .models import Evento, TipoEvento, StatusEvento

class EventListView(ListView):
    model = Evento
    template_name = 'events/event_list.html'
    context_object_name = 'evento_list'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Evento.objects.all().order_by('data_inicio')
        
        # Filtros
        tipo = self.request.GET.get('tipo')
        status = self.request.GET.get('status')
        
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

class EventDetailView(DetailView):
    model = Evento
    template_name = 'events/event_detail.html'
    context_object_name = 'evento'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Evento
    template_name = 'events/event_form.html'
    fields = ['titulo', 'slug', 'descricao', 'tipo', 'data_inicio', 'data_fim', 
              'local', 'endereco', 'capacidade_maxima', 'inscricao_obrigatoria', 
              'imagem', 'status']
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        form.instance.organizador = self.request.user
        
        # Verificar qual ação foi solicitada
        action = self.request.POST.get('action')
        if action == 'draft':
            form.instance.status = StatusEvento.CANCELADO  # Usar como rascunho
        elif action == 'schedule':
            form.instance.status = StatusEvento.AGENDADO
        
        messages.success(self.request, 'Evento criado com sucesso!')
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Evento
    template_name = 'events/event_form.html'
    fields = ['titulo', 'slug', 'descricao', 'tipo', 'data_inicio', 'data_fim', 
              'local', 'endereco', 'capacidade_maxima', 'inscricao_obrigatoria', 
              'imagem', 'status']
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        # Verificar qual ação foi solicitada
        action = self.request.POST.get('action')
        if action == 'draft':
            form.instance.status = StatusEvento.CANCELADO  # Usar como rascunho
        elif action == 'schedule':
            form.instance.status = StatusEvento.AGENDADO
        
        messages.success(self.request, 'Evento atualizado com sucesso!')
        return super().form_valid(form)

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Evento
    template_name = 'events/event_confirm_delete.html'
    context_object_name = 'evento'
    success_url = reverse_lazy('events:list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Evento excluído com sucesso!')
        return super().delete(request, *args, **kwargs)