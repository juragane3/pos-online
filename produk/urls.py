# produk/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_produk, name='daftar_produk'),
    path('kasir/', views.halaman_kasir, name='halaman_kasir'),
    path('proses_transaksi/', views.proses_transaksi, name='proses_transaksi'),
    # PASTIKAN BARIS INI ADA DAN SUDAH DISIMPAN (SAVE)
    path('laporan/', views.laporan_penjualan, name='laporan_penjualan'),
]