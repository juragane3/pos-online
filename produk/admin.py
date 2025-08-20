# produk/admin.py

from django.contrib import admin
from .models import Produk, Transaksi, DetailTransaksi

# Kelas ini akan mengatur tampilan DetailTransaksi di dalam Transaksi
class DetailTransaksiInline(admin.TabularInline):
    model = DetailTransaksi
    extra = 1 # Jumlah baris kosong untuk detail baru

# Kelas ini akan mengatur tampilan utama untuk Transaksi
class TransaksiAdmin(admin.ModelAdmin):
    # Menampilkan detail transaksi langsung di halaman transaksi
    inlines = [DetailTransaksiInline]
    # Kolom yang ingin ditampilkan di daftar semua transaksi
    list_display = ('id', 'waktu_transaksi', 'total_harga')
    # Menambahkan filter berdasarkan tanggal
    list_filter = ['waktu_transaksi']

# Daftarkan model Anda dengan kelas kustom di atas
admin.site.register(Produk)
admin.site.register(Transaksi, TransaksiAdmin) # Gunakan TransaksiAdmin
admin.site.register(DetailTransaksi)