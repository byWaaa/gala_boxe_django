from django.urls import path
from . import views

app_name = 'gala'

urlpatterns = [
    path('', views.acceuil, name='acceuil'),
    path('inscription/', views.inscription, name='inscription'),
]

