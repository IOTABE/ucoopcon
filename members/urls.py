from django.urls import path
from . import views
from .views import PessoaCreateView, PessoaListView, PessoaDetailView, CriarMembroView, ficha_cadastro_pdf_view, termo_adesao_pdf_view

app_name = 'members'

urlpatterns = [
    # URLs para membros
    path('', views.MembroListView.as_view(), name='list'),
    path('novo/', views.MembroCreateView.as_view(), name='create'),
    path('<int:pk>/', views.MembroDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.MembroUpdateView.as_view(), name='update'),
    path('<int:pk>/deletar/', views.MembroDeleteView.as_view(), name='delete'),
    
    # URLs para contribuições
    path('contribuicoes/', views.ContribuicaoListView.as_view(), name='contribuicoes'),
    path('contribuicoes/nova/', views.ContribuicaoCreateView.as_view(), name='contribuicao_create'),
    path('contribuicoes/<int:pk>/', views.ContribuicaoDetailView.as_view(), name='contribuicao_detail'),
    path('contribuicoes/<int:pk>/editar/', views.ContribuicaoUpdateView.as_view(), name='contribuicao_update'),
    path('contribuicoes/<int:pk>/deletar/', views.ContribuicaoDeleteView.as_view(), name='contribuicao_delete'),
    
    # URLs para perfil do membro (se logado)
    path('perfil/', views.MembroDetailView.as_view(), name='profile'),
    
    # URLs básicas para relatórios
    path('relatorios/membros/', views.member_report_view, name='member_report'),
    path('relatorios/contribuicoes/', views.contribution_report_view, name='contribution_report'),
    path('relatorios/ativos/', views.active_members_report_view, name='active_members_report'),
    path('relatorios/inativos/', views.inactive_members_report_view, name='inactive_members_report'),
    path('relatorios/suspensos/', views.suspended_members_report_view, name='suspended_members_report'),
    path('relatorios/tipos/', views.member_types_report_view, name='member_types_report'),
    path('relatorios/adesao/', views.membership_adhesion_report_view, name='membership_adhesion_report'),
    path('relatorios/contribuicoes/mensais/', views.monthly_contributions_report_view, name='monthly_contributions_report'),
    path('relatorios/contribuicoes/anuais/', views.yearly_contributions_report_view, name='yearly_contributions_report'),
    path('relatorios/contribuicoes/periodo/', views.periodic_contributions_report_view, name='periodic_contributions_report'),
    
    # Novas URLs para pessoas
    path('pessoas/', PessoaListView.as_view(), name='pessoa_list'),
    path('pessoas/novo/', PessoaCreateView.as_view(), name='pessoa_create'),
    path('pessoas/<int:pk>/', PessoaDetailView.as_view(), name='pessoa_detail'),
    
    # URL para tornar uma pessoa um membro
    path('pessoas/<int:pessoa_pk>/tornar-membro/', CriarMembroView.as_view(), name='criar_membro'),
    
    # URL para ficha de cadastro em PDF
    path('membro/<int:pk>/ficha-cadastro/', ficha_cadastro_pdf_view, name='ficha_cadastro_pdf'),
    
    # URL para termo de adesão em PDF
    path('membro/<int:pk>/termo-adesao/', termo_adesao_pdf_view, name='termo_adesao_pdf'),
]