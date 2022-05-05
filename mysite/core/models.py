from django.db import models


class Book(models.Model):
    message = models.CharField(max_length=500)
    key = models.CharField(max_length=100)
    image = models.FileField(upload_to='books/pdfs/')
    # cover = models.ImageField(upload_to='books/covers/', null=True, blank=True)

    def __str__(self):
        return self.message

    def delete(self, *args, **kwargs):
        self.image.delete()
        # self.cover.delete()
        super().delete(*args, **kwargs)

class Book1(models.Model):
    image = models.FileField(upload_to='books/pdfs1/')
    key = models.CharField(max_length=100)

    def __str__(self):
        return self.key
