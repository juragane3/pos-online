# produk/views.py

# ... (import dan fungsi daftar_produk biarkan saja) ...

def halaman_kasir(request):
    semua_produk = Produk.objects.all()
    context = {
        'semua_produk': semua_produk,
    }
    return render(request, 'produk/kasir.html', context)