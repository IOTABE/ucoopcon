from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from .models import Membro, Contribuicao, Pessoas
from .forms import MembroForm, ContribuicaoForm, MembroSearchForm, ContribuicaoSearchForm, PessoaForm
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
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import date

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

class PessoaCreateView(CreateView):
    model = Pessoas
    form_class = PessoaForm
    template_name = 'members/pessoa_form.html'
    success_url = reverse_lazy('members:pessoa_list')

class PessoaListView(ListView):
    model = Pessoas
    template_name = 'members/pessoa_list.html'
    context_object_name = 'pessoas'

class PessoaDetailView(DetailView):
    model = Pessoas
    template_name = 'members/pessoa_detail.html'
    context_object_name = 'pessoa'

class CriarMembroView(CreateView):
    model = Membro
    form_class = MembroForm
    template_name = 'members/membro_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.pessoa = get_object_or_404(Pessoas, pk=kwargs['pessoa_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.pessoa = self.pessoa
        # Geração automática do número do membro
        ultimo = Membro.objects.order_by('-id').first()
        proximo_numero = 1 if not ultimo else int(ultimo.numero_membro) + 1
        form.instance.numero_membro = str(proximo_numero).zfill(6)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('members:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pessoa'] = self.pessoa
        return context

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

def ficha_cadastro_pdf_view(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    pessoa = membro.pessoa

    # Exemplo de como montar os dados de parcelas (ajuste conforme seu model)
    # Aqui, supõe-se que exista uma relação de contribuições/parcelas para o membro
    parcelas = Contribuicao.objects.filter(membro=membro).order_by('data_pagamento')
    parcelas_list = []
    total = 0
    for idx, parcela in enumerate(parcelas, 1):
        total += parcela.valor
        parcelas_list.append({
            'numero': idx,
            'forma_pagamento': parcela.get_tipo_display() if hasattr(parcela, 'get_tipo_display') else parcela.tipo,
            'vencimento': parcela.data_pagamento,
            'valor': f"{parcela.valor:.2f}",
            'total': f"{total:.2f}",
        })

    # Contexto para o template
    context = {
        'membro': membro,
        'parcelas_list': parcelas_list,
        # Adicione outros dados necessários para o template
    }

    html_string = render_to_string('members/ficha_cadastro.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="ficha_cadastro_{membro.numero_membro}.pdf"'
    return response

def termo_adesao_pdf_view(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    
    # Se o campo data_adesao não existir, use outro campo de data ou a data atual
    data_adesao = getattr(membro, 'data_adesao', None)
    if not data_adesao:
        from datetime import date
        data_adesao = date.today()
    
    # Se quiser gerar um QR Code, gere a URL/base64 e passe como 'url_qrcode'
    # Exemplo: url_qrcode = gerar_qrcode_url(membro)
    url_qrcode = None  # ou gere conforme sua lógica

    context = {
        'membro': membro,
        'url_qrcode': url_qrcode,
        # Adicione outros dados se necessário
    }

    html_string = render_to_string('members/termo_adesao.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="termo_adesao_{membro.numero_membro}.pdf"'
    return response
