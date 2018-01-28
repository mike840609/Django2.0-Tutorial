#!-*-encoding:utf-8-*-
from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre



# function base


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # counter
    time = getTime()
    count = getCount()


    return render(request,
                  'index.html',
                  context={'num_books': num_books,
                           'num_instances': num_instances,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors,
                           'num_visits': num_visits,
                           'count' : count,
                           'time':time})


from django.views import generic
# class base


class BookListView(generic.ListView):
    model = Book
    # Pagination
    # the number of items show on one page 
    paginate_by = 6


    '''
    # You can add attributes to change the default behaviour above.
    # your own name for the list as a template variable
    context_object_name = 'my_book_list'
    queryset = Book.objects.filter(title__icontains='war')[:5]  # Get 5 books containing the title war

    # Specify your own template name/location
    template_name = 'books/my_arbitrary_template_name_list.html'
    '''

    # Overriding methods in class-based views    
    '''
    def get_queryset(self):
        return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    '''

class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 6


class AuthorDetailView(generic.DetailView):
    model = Author


# counter ==============================================================================================
import time
from django.template import loader,Context
import pickle as pk
import os.path

def getTime():#获取当前时间

    return time.ctime()

def getCount(): 

    count_file_name = 'count.p'
    count = 0

    if  os.path.exists(count_file_name)==True:
        count = pk.load(open(count_file_name, 'rb'))
        count += 1
        pk.dump(count,open(count_file_name,'wb'))
    else :
        pk.dump( count , open(count_file_name,"wb"))

    return count
