# produk/views.py

from django.shortcuts import render
from .models import Produk, Transaksi, DetailTransaksi
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # <-- INI YANG PERLU DITAMBAHKAN
import json
from django.db import transaction

# ... (fungsi daftar_produk dan halaman_kasir) ...
def daftar_produk(request):
    semua_produk = Produk.objects.all()
    context = {
        'semua_produk': semua_produk,
    }
    return render(request, 'produk/daftar_produk.html', context)

def halaman_kasir(request):
    semua_produk = Produk.objects.all()
    context = {
        'semua_produk': semua_produk,
    }
    return render(request, 'produk/kasir.html', context)

@csrf_exempt
@transaction.atomic
def proses_transaksi(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('keranjang', {})
            total_harga = data.get('total', 0)

            transaksi_baru = Transaksi.objects.create(total_harga=total_harga)

            for nama_produk, detail in items.items():
                try:
                    produk = Produk.objects.get(nama=nama_produk)
                    
                    DetailTransaksi.objects.create(
                        transaksi=transaksi_baru,
                        produk=produk,
                        jumlah=detail['jumlah'],
                        subtotal=detail['harga'] * detail['jumlah']
                    )
                    
                    produk.stok -= detail['jumlah']
                    produk.save()

                except Produk.DoesNotExist:
                    transaction.set_rollback(True)
                    return JsonResponse({'status': 'error', 'message': f'Produk {nama_produk} tidak ditemukan'}, status=404)

            return JsonResponse({'status': 'success', 'message': 'Transaksi berhasil disimpan!', 'transaksi_id': transaksi_baru.id})
        
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan'}, status=405)
@csrf_exempt # Sebaiknya gunakan metode CSRF yang lebih aman di produksi
@transaction.atomic # Menjamin semua operasi database berhasil atau tidak sama sekali
def proses_transaksi(request):
    if request.method == 'POST':
        try:
            # Ambil data mentah dari body request
            data = json.loads(request.body)

            # Ambil item keranjang dan total harga dari data
            items = data.get('keranjang', {})
            total_harga = data.get('total', 0)

            # 1. Buat objek Transaksi utama
            transaksi_baru = Transaksi.objects.create(total_harga=total_harga)

            # 2. Loop melalui setiap item di keranjang untuk membuat DetailTransaksi
            for nama_produk, detail in items.items():
                try:
                    # Ambil objek produk dari database berdasarkan nama
                    produk = Produk.objects.get(nama=nama_produk)

                    # Buat objek DetailTransaksi
                    DetailTransaksi.objects.create(
                        transaksi=transaksi_baru,
                        produk=produk,
                        jumlah=detail['jumlah'],
                        subtotal=detail['harga'] * detail['jumlah']
                    )

                    # (Opsional) Kurangi stok produk
                    produk.stok -= detail['jumlah']
                    produk.save()

                except Produk.DoesNotExist:
                    # Jika produk tidak ditemukan, batalkan transaksi
                    transaction.set_rollback(True)
                    return JsonResponse({'status': 'error', 'message': f'Produk {nama_produk} tidak ditemukan'}, status=404)

            # Jika semua berhasil, kirim respons sukses
            return JsonResponse({'status': 'success', 'message': 'Transaksi berhasil disimpan!', 'transaksi_id': transaksi_baru.id})

        except Exception as e:
            # Jika ada error lain, batalkan transaksi
            transaction.set_rollback(True)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # Jika bukan metode POST, tolak permintaan
    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan'}, status=405)
def laporan_penjualan(request):
    # Ambil semua objek transaksi, urutkan dari yang terbaru
    semua_transaksi = Transaksi.objects.all().order_by('-waktu_transaksi')

    context = {
        'semua_transaksi': semua_transaksi,
    }

    return render(request, 'produk/laporan.html', context)
