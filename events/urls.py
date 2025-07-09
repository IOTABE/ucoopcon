from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('novo/', views.EventCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.EventDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.EventUpdateView.as_view(), name='update'),
    path('<int:pk>/deletar/', views.EventDeleteView.as_view(), name='delete'),
]