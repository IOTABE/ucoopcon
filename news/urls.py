from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='list'),
    path('nova/', views.NewsCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.NewsUpdateView.as_view(), name='update'),
    path('<int:pk>/deletar/', views.NewsDeleteView.as_view(), name='delete'),
]