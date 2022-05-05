from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mysite.core import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/upload/', views.upload_book, name='upload_book'),
    path('books1/', views.book_list1, name='book_list1'),
    path('books1/upload1/', views.upload_book1, name='upload_book1'),
    path('books/<int:pk>/', views.external, name='delete_book'),
    path('books1/<int:pk>/', views.external1, name='delete_book1'),
    # path('books1/<int:pk>/', views.delete_book1, name='delete_book1'),
    # path('books/<int:pk>/', views.delete_book, name='delete_book'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
