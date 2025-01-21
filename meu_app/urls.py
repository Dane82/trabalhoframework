from django.urls import path
from . import views

urlpatterns = [
    path('carregar/', views.carregar_dados, name='carregar_dados'),
]
