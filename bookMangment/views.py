from django.shortcuts import get_object_or_404, render
from .models import *

# Create your views here.

def index(request):
    bookList = Book.objects.all()
    context = {'bookList': bookList}

    return render(request, 'book_list.html', context)
def detail(request,pk):
    book = get_object_or_404(Book, pk=pk)
    context = {'book': book}

    return render(request, 'book_detail.html', context)

def home(request):
    return render(request, 'home.html')
