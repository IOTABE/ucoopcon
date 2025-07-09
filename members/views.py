from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from .models import Membro, Contribuicao
from .forms import MembroForm, ContribuicaoForm, MembroSearchForm, ContribuicaoSearchForm
from .reports import (generate_member_report, 
                    generate_contribution_report, 
                    generate_active_members_report, 
                    generate_inactive_members_report, 
                    generate_suspended_members_report, 
                    generate_member_types_report, 
                    generate_membership_adhesion_report, 
                    generate_monthly_contributions_report,    
                    generate_yearly_contributions_report, 
                    generate_periodic_contributions_report, 
                    generate_contributions_by_member_report, 
                    generate_contributions_by_month_report, 
                    generate_contributions_by_year_report, 
                    generate_contributions_by_period_report, 
                    generate_contributions_by_type_report, 
                    generate_contributions_by_status_report, 
                    generate_contributions_by_date_report, 
                    generate_contributions_by_month_year_report,
                    generate_contributions_by_member_month_report, 
                    generate_contributions_by_member_year_report, 
                    generate_contributions_by_member_period_report, 
                    generate_contributions_by_member_type_report, 
                    generate_contributions_by_member_status_report, 
                    generate_contributions_by_member_date_report, 
                    generate_contributions_by_member_month_year_report, 
                    generate_contributions_by_member_month_year_period_report, 
                    generate_contributions_by_member_month_year_type_report, 
                    generate_contributions_by_member_month_year_status_report, 
                    generate_contributions_by_member_month_year_date_report, 
                    generate_contributions_by_member_month_year_type_status_report, 
                    generate_contributions_by_member_month_year_type_date_report, 
                    generate_contributions_by_member_month_year_type_period_report, 
                    generate_contributions_by_member_month_year_status_date_report, 
                    generate_contributions_by_member_month_year_status_period_report, 
                    generate_contributions_by_member_month_year_date_period_report, 
                    generate_contributions_by_member_month_year_type_status_date_report, 
                    generate_contributions_by_member_month_year_type_status_period_report, 
                    generate_contributions_by_member_month_year_type_date_period_report, 
                    generate_contributions_by_member_month_year_status_date_period_report)

class MembroListView(LoginRequiredMixin, ListView):
    model = Membro
    template_name = 'members/membro_list.html'
    context_object_name = 'membros'
    paginate_by = 20

    def get_queryset(self):
        queryset = Membro.objects.all()
        search_form = MembroSearchForm(self.request.GET)
        
        if search_form.is_valid():
            nome = search_form.cleaned_data.get('nome')
            cpf = search_form.cleaned_data.get('cpf')
            ativo = search_form.cleaned_data.get('ativo')
            data_nascimento_inicio = search_form.cleaned_data.get('data_nascimento_inicio')
            data_nascimento_fim = search_form.cleaned_data.get('data_nascimento_fim')
            
            if nome:
                queryset = queryset.filter(
                    Q(user__first_name__icontains=nome) | 
                    Q(user__last_name__icontains=nome) |
                    Q(nome__icontains=nome)
                )
            if cpf:
                queryset = queryset.filter(cpf__icontains=cpf)
            if ativo is not None:
                queryset = queryset.filter(ativo=ativo)
            if data_nascimento_inicio:
                queryset = queryset.filter(data_nascimento__gte=data_nascimento_inicio)
            if data_nascimento_fim:
                queryset = queryset.filter(data_nascimento__lte=data_nascimento_fim)
        
        return queryset.order_by('user__first_name', 'user__last_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = MembroSearchForm(self.request.GET)
        return context

class MembroDetailView(LoginRequiredMixin, DetailView):
    model = Membro
    template_name = 'members/membro_detail.html'
    context_object_name = 'membro'

class MembroCreateView(LoginRequiredMixin, CreateView):
    model = Membro
    form_class = MembroForm
    template_name = 'members/membro_form.html'
    success_url = reverse_lazy('members:list')

    def form_valid(self, form):
        messages.success(self.request, 'Membro criado com sucesso!')
        return super().form_valid(form)

class MembroUpdateView(LoginRequiredMixin, UpdateView):
    model = Membro
    form_class = MembroForm
    template_name = 'members/membro_form.html'
    success_url = reverse_lazy('members:list')

    def form_valid(self, form):
        messages.success(self.request, 'Membro atualizado com sucesso!')
        return super().form_valid(form)

class MembroDeleteView(LoginRequiredMixin, DeleteView):
    model = Membro
    template_name = 'members/membro_confirm_delete.html'
    success_url = reverse_lazy('members:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Membro excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

class ContribuicaoListView(LoginRequiredMixin, ListView):
    model = Contribuicao
    template_name = 'members/contribuicao_list.html'
    context_object_name = 'contribuicoes'
    paginate_by = 20

    def get_queryset(self):
        queryset = Contribuicao.objects.all()
        search_form = ContribuicaoSearchForm(self.request.GET)
        
        if search_form.is_valid():
            membro = search_form.cleaned_data.get('membro')
            data_inicio = search_form.cleaned_data.get('data_inicio')
            data_fim = search_form.cleaned_data.get('data_fim')
            valor_minimo = search_form.cleaned_data.get('valor_minimo')
            valor_maximo = search_form.cleaned_data.get('valor_maximo')
            tipo = search_form.cleaned_data.get('tipo')
            status = search_form.cleaned_data.get('status')
            
            if membro:
                queryset = queryset.filter(membro=membro)
            if data_inicio:
                queryset = queryset.filter(data_pagamento__gte=data_inicio)
            if data_fim:
                queryset = queryset.filter(data_pagamento__lte=data_fim)
            if valor_minimo:
                queryset = queryset.filter(valor__gte=valor_minimo)
            if valor_maximo:
                queryset = queryset.filter(valor__lte=valor_maximo)
            if tipo:
                queryset = queryset.filter(tipo=tipo)
            if status:
                queryset = queryset.filter(status=status)
        
        return queryset.order_by('-data_pagamento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ContribuicaoSearchForm(self.request.GET)
        return context

class ContribuicaoDetailView(LoginRequiredMixin, DetailView):
    model = Contribuicao
    template_name = 'members/contribuicao_detail.html'
    context_object_name = 'contribuicao'

class ContribuicaoCreateView(LoginRequiredMixin, CreateView):
    model = Contribuicao
    form_class = ContribuicaoForm
    template_name = 'members/contribuicao_form.html'
    success_url = reverse_lazy('members:contribuicoes')

    def form_valid(self, form):
        messages.success(self.request, 'Contribuição criada com sucesso!')
        return super().form_valid(form)

class ContribuicaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Contribuicao
    form_class = ContribuicaoForm
    template_name = 'members/contribuicao_form.html'
    success_url = reverse_lazy('members:contribuicoes')

    def form_valid(self, form):
        messages.success(self.request, 'Contribuição atualizada com sucesso!')
        return super().form_valid(form)

class ContribuicaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Contribuicao
    template_name = 'members/contribuicao_confirm_delete.html'
    success_url = reverse_lazy('members:contribuicoes')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Contribuição excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# Views para relatórios
def member_report_view(request):
    """View para relatório de membros"""
    if request.method == 'POST':
        return generate_member_report(request)
    return render(request, 'members/reports/member_report.html')

def contribution_report_view(request):
    """View para relatório de contribuições"""
    if request.method == 'POST':
        return generate_contribution_report(request)
    return render(request, 'members/reports/contribution_report.html')

def active_members_report_view(request):
    """View para relatório de membros ativos"""
    if request.method == 'POST':
        return generate_active_members_report(request)
    return render(request, 'members/reports/active_members_report.html')

def inactive_members_report_view(request):
    """View para relatório de membros inativos"""
    if request.method == 'POST':
        return generate_inactive_members_report(request)
    return render(request, 'members/reports/inactive_members_report.html')

def suspended_members_report_view(request):
    """View para relatório de membros suspensos"""
    if request.method == 'POST':
        return generate_suspended_members_report(request)
    return render(request, 'members/reports/suspended_members_report.html')

def member_types_report_view(request):
    """View para relatório por tipos de membro"""
    if request.method == 'POST':
        return generate_member_types_report(request)
    return render(request, 'members/reports/member_types_report.html')

def membership_adhesion_report_view(request):
    """View para relatório de adesões"""
    if request.method == 'POST':
        return generate_membership_adhesion_report(request)
    return render(request, 'members/reports/membership_adhesion_report.html')

def monthly_contributions_report_view(request):
    """View para relatório de contribuições mensais"""
    if request.method == 'POST':
        return generate_monthly_contributions_report(request)
    return render(request, 'members/reports/monthly_contributions_report.html')

def yearly_contributions_report_view(request):
    """View para relatório de contribuições anuais"""
    if request.method == 'POST':
        return generate_yearly_contributions_report(request)
    return render(request, 'members/reports/yearly_contributions_report.html')

def periodic_contributions_report_view(request):
    """View para relatório de contribuições por período"""
    if request.method == 'POST':
        return generate_periodic_contributions_report(request)
    return render(request, 'members/reports/periodic_contributions_report.html')
