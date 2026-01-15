from django.shortcuts import render
from django.views import generic

from catalog.models import Book, BookInstance, Author


# Create your views here.

def index(request):
    num_books = Book.objects.all().count()
    num_instances = Book.objects.all().count()
    num_instances_available = (BookInstance.objects.filter(status__exact='a').count())
    num_authors = Author.objects.count()
    context = {'num_books': num_books, 'num_instances': num_instances,
               'num_instances_available': num_instances_available, 'num_authors': num_authors
               }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    context_object_name = 'book_list'
    queryset = Book.objects.filter(title__icontains='node')
    template_name = 'bools/my_arbitrary_template_name_list.html'
    model = Book
