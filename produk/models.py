# produk/models.py

from django.db import models
from django.utils import timezone # <-- THIS LINE WAS MISSING

class Produk(models.Model):
    nama = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nama

class Transaksi(models.Model):
    waktu_transaksi = models.DateTimeField(default=timezone.now)
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Transaksi #{self.id} - {self.waktu_transaksi.strftime('%Y-%m-%d %H:%M')}"

class DetailTransaksi(models.Model):
    transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE, related_name='detail')
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produk.nama} (x{self.jumlah})"