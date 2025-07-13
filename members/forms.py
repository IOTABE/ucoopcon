from django import forms
from .models import Membro, Contribuicao, TipoContribuicao, StatusContribuicao
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.utils import timezone

class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = [
            'user',
            'pessoa',
            'numero_membro',
            'tipo_membro',
            'status',
            'ficha_cadastral_numero',
            'term_adesao_numero',
            'data_adesao',
            'foto',
            'ativo',
        ]
        
class ContribuicaoForm(forms.ModelForm):
    class Meta:
        model = Contribuicao
        fields = ['membro', 'data_pagamento', 'descricao', 'mes_referencia', 'valor', 'tipo', 'status']      
        
class MembroSearchForm(forms.Form):
    nome = forms.CharField(required=False, label='Nome')
    cpf = forms.CharField(required=False, label='CPF')
    ativo = forms.BooleanField(required=False, label='Ativo')
    data_nascimento_inicio = forms.DateField(required=False, label='Data de Nascimento (Início)')
    data_nascimento_fim = forms.DateField(required=False, label='Data de Nascimento (Fim)') 
    
class ContribuicaoSearchForm(forms.Form):
    membro = forms.ModelChoiceField(queryset=Membro.objects.all(), required=False, label='Membro')
    data_inicio = forms.DateField(required=False, label='Data (Início)')
    data_fim = forms.DateField(required=False, label='Data (Fim)')
    valor_minimo = forms.DecimalField(required=False, label='Valor Mínimo', decimal_places=2)
    valor_maximo = forms.DecimalField(required=False, label='Valor Máximo', decimal_places=2)
    tipo = forms.ChoiceField(choices=[('', 'Selecione um tipo')] + list(TipoContribuicao.choices), required=False, label='Tipo')
    status = forms.ChoiceField(choices=[('', 'Selecione um status')] + list(StatusContribuicao.choices), required=False, label='Status')
    
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim') 
        if data_inicio and data_fim and data_inicio > data_fim:
            raise forms.ValidationError(
                "A data de início não pode ser maior que a data de fim."
            )
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['membro'].empty_label = "Selecione um membro"

    def get_membro_choices(self):
        return Membro.objects.all().values_list('id', 'user__username')

    def get_tipo_choices(self):
        return TipoContribuicao.choices
    
    def get_status_choices(self):
        return StatusContribuicao.choices
    
class MembroSearchFormDuplicated(forms.Form):
    nome = forms.CharField(required=False, label='Nome')
    cpf = forms.CharField(required=False, label='CPF')
    ativo = forms.BooleanField(required=False, label='Ativo')
    data_nascimento_inicio = forms.DateField(required=False, label='Data de Nascimento (Início)')
    data_nascimento_fim = forms.DateField(required=False, label='Data de Nascimento (Fim)')
    
    def clean(self):
        cleaned_data = super().clean()
        data_nascimento_inicio = cleaned_data.get('data_nascimento_inicio')
        data_nascimento_fim = cleaned_data.get('data_nascimento_fim')
        
        if data_nascimento_inicio and data_nascimento_fim and data_nascimento_inicio > data_nascimento_fim:
            raise forms.ValidationError(
                "A data de nascimento inicial não pode ser maior que a data de nascimento final."
            )
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ativo'].required = False
        self.fields['ativo'].label = 'Ativo'
        self.fields['ativo'].initial = True  # Default to True if not specified
        self.fields['nome'].widget.attrs.update({'placeholder': 'Digite o nome do membro'})
        self.fields['cpf'].widget.attrs.update({'placeholder': 'Digite o CPF do membro'})
        self.fields['data_nascimento_inicio'].widget.attrs.update({'placeholder': 'Data de Nascimento (Início)'})
        self.fields['data_nascimento_fim'].widget.attrs.update({'placeholder': 'Data de Nascimento (Fim)'})

    def get_membro_choices(self):
        return Membro.objects.all().values_list('id', 'user__username')

    def get_tipo_choices(self):
        return TipoContribuicao.choices
    
    def get_status_choices(self):
        return StatusContribuicao.choices

    def get_membro_queryset(self):
        return Membro.objects.all()
