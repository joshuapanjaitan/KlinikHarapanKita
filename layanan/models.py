from django.db import models

# Create your models here.
# setiap mengedit model harus migrasi dlu


class Antrian(models.Model):
    code_layanan = models.CharField(max_length=2)
    nama_layanan = models.CharField(max_length=100)
    deskripsi = models.TextField()
    foto = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.id)


class Current(models.Model):
    no_antrian = models.IntegerField()
    jenis_layanan = models.CharField(max_length=2)
    status = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.no_antrian)
