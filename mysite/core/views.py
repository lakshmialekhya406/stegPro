from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import BookForm,Book1Form
from .models import Book, Book1

import sys
from subprocess import run,PIPE


class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })

def book_list1(request):
    books = Book1.objects.all()
    return render(request, 'book1_list.html', {
        'books': books
    })


def upload_book1(request):
    if request.method == 'POST':
        form = Book1Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list1')
    else:
        form = Book1Form()
    return render(request, 'upload_book1.html', {
        'form': form
    })

def delete_book1(request, pk):
    if request.method == 'POST':
        book = Book1.objects.get(pk=pk)
        book.delete()
    return redirect('book_list1')

def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        print(book.image)
        book.delete()
    return redirect('book_list')

def external(request, pk):
    books = Book.objects.get(pk=pk)
    img = books.image.url
    message = books.message
    password = books.key

    a=list(img.split('/'))
    b = "C:\\Users\\dell\\Desktop\\major\\media\\books\\pdfs" + "\\" + a[-1]

    out = run([sys.executable,'C:\\Users\\dell\\Desktop\\major\\exp.py',message,password,b],shell=False,stdout=PIPE)
    
    x=out.stdout
    print(b)
    if(x==b'\r\nAn error occured\r\n'):
        ans = "An error occured"
    else:
        ans = out.stdout.decode('utf-8')
    books.delete()
    return render(request,'home.html',{'data':ans})


def external1(request, pk):
    books = Book1.objects.get(pk=pk)
    img = books.image.url
    
    password = books.key

    a=list(img.split('/'))
    b = "C:\\Users\\dell\\Desktop\\major\\media\\books\\pdfs1" + "\\" + a[-1]

    out = run([sys.executable,'C:\\Users\\dell\\Desktop\\major\\dex.py',password,b],shell=False,stdout=PIPE)
    x=out.stdout
    print(out.stdout)
    if(x==b'\r\nWrong password!\r\n'):
        ans = "Wrong password"
    elif(x==b'\r\nAn error occured\r\n'):
        ans = "An error occured"
    elif(x==b'\r\nInvalid data!\r\n'):
        ans = "Invalid data"
    else:
        ans = out.stdout.decode('utf-8')
    books.delete()
    return render(request,'home.html',{'data1': ans})
