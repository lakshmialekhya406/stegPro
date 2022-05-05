from django import forms

from .models import Book, Book1


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('message', 'key', 'image')

class Book1Form(forms.ModelForm):
    class Meta:
        model = Book1
        fields = ('image','key')

