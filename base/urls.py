# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('prospectus', views.prospectus, name='prospectus'),
    path('success', views.success, name='success'),
    path('proof', views.proof, name='proof'),
]