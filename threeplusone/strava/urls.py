from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('input', views.input, name='input'),
    path('results', views.results, name='results'),
]