from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import F
from .models import Noticia, Categoria, StatusNoticia

def index(request):
    categorias = Categoria.objects.all()
    status_noticias = StatusNoticia.objects.all()
    noticias = Noticia.objects.all()

    context = {
        'categorias': categorias,
        'status_noticias': status_noticias,
        'noticias': noticias,
    }

    return render(request, 'news/index.html', context)  

def categoria_detail(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    noticias = Noticia.objects.filter(categoria=categoria)

    context = {
        'categoria': categoria,
        'noticias': noticias,
    }

    return render(request, 'news/categoria_detail.html', context)

def noticia_detail(request, noticia_id):
    noticia = Noticia.objects.get(id=noticia_id)

    context = {
        'noticia': noticia,
    }

    return render(request, 'news/noticia_detail.html', context) 

class NewsListView(ListView):
    model = Noticia
    template_name = 'news/news_list.html'
    context_object_name = 'noticia_list'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Noticia.objects.filter(status=StatusNoticia.PUBLICADA).order_by('-data_publicacao')
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context

class NewsDetailView(DetailView):
    model = Noticia
    template_name = 'news/news_detail.html'
    context_object_name = 'noticia'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Noticia.objects.filter(status=StatusNoticia.PUBLICADA)
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Incrementar visualizações
        Noticia.objects.filter(pk=obj.pk).update(visualizacoes=F('visualizacoes') + 1)
        obj.refresh_from_db()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Notícias relacionadas (mesma categoria, exceto a atual)
        if self.object.categoria:
            context['noticias_relacionadas'] = Noticia.objects.filter(
                categoria=self.object.categoria,
                status=StatusNoticia.PUBLICADA
            ).exclude(pk=self.object.pk)[:4]
        return context

class NewsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Noticia
    template_name = 'news/news_form.html'
    fields = ['titulo', 'slug', 'resumo', 'conteudo', 'categoria', 'imagem_destaque', 'destaque', 'status']
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        
        # Verificar qual ação foi solicitada
        action = self.request.POST.get('action')
        if action == 'draft':
            form.instance.status = StatusNoticia.RASCUNHO
        elif action == 'publish':
            form.instance.status = StatusNoticia.PUBLICADA
        
        messages.success(self.request, 'Notícia criada com sucesso!')
        return super().form_valid(form)

class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Noticia
    template_name = 'news/news_form.html'
    fields = ['titulo', 'slug', 'resumo', 'conteudo', 'categoria', 'imagem_destaque', 'destaque', 'status']
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        # Verificar qual ação foi solicitada
        action = self.request.POST.get('action')
        if action == 'draft':
            form.instance.status = StatusNoticia.RASCUNHO
        elif action == 'publish':
            form.instance.status = StatusNoticia.PUBLICADA
        
        messages.success(self.request, 'Notícia atualizada com sucesso!')
        return super().form_valid(form)

class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Noticia
    template_name = 'news/news_confirm_delete.html'
    context_object_name = 'noticia'
    success_url = reverse_lazy('news:list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Notícia excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


