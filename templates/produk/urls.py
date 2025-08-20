# produk/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_produk, name='daftar_produk'),
    # Ensure this new line is present and saved
    path('kasir/', views.halaman_kasir, name='halaman_kasir'),
]