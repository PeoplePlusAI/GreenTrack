from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_products, name='search'),
    path('upload', views.upload_invoice, name='upload')
]
