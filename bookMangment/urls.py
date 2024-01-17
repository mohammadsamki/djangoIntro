from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('book/', index, name='bookList'), # ''= ( mean root page)
    #  book_detail url
    path('book/<int:pk>/', detail, name='book_detail'),
]
