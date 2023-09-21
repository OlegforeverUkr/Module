from django.shortcuts import render, redirect
from .models import Book, Author, BorrowRequest
from django.views.generic import ListView, DetailView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic.edit import CreateView
from .forms import CreateBookForm
from datetime import datetime, timedelta


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'



@method_decorator(login_required, name='dispatch')
class BorrowListView(ListView):
    model = BorrowRequest
    template_name = 'borrow_list.html'
    context_object_name = 'borrow_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return BorrowRequest.objects.all()
        else:
            return BorrowRequest.objects.filter(borrower=user)



class BorrowRequestView(DetailView):
    model = Book
    template_name = 'borrow_request.html'
    http_method_names = ['get', 'post']
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        try:
            borrow_request = BorrowRequest.objects.filter(book=context['book'], borrower=context['user']).last()
            context['borrow_request'] = borrow_request
        except BorrowRequest.DoesNotExist:
            context['borrow_request'] = None
        return context

    def post(self, request, *args, **kwargs):
        try:
            book = Book.objects.get(id=self.kwargs['pk'])
            borrower = request.user
            action = request.POST.get('action')

            if action == 'request':
                book.is_available = False
                book.book_borrower = borrower
                book.save()
                BorrowRequest.objects.create(book=book, borrower=borrower, status=1)

            elif action == 'collect':
                borrow_request = book.borrow_requests.filter(book=book, borrower=borrower).last()
                borrow_request.status = 3
                borrow_request.due_date = datetime.now().date() + timedelta(days=7)
                borrow_request.save()

            elif action == 'return':
                book.book_borrower = None
                book.save()
                borrow_request = book.borrow_requests.filter(book=book, borrower=borrower).last()
                borrow_request.status = 4
                borrow_request.complete_date = datetime.now().date()
                borrow_request.save()

            url = reverse('booksapp:home_page')
            return HttpResponseRedirect(url)
        except Book.DoesNotExist:
            raise Http404('This book is not found')




class CreateBookView(CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = 'book_create.html'  

    def get_success_url(self):
        return reverse('booksapp:home_page')


class SearchResultsView(View):
    template_name = 'search_results.html'

    def get(self, request):
        query = request.GET.get('query')
        if query:
            search_results = Book.objects.filter(book_title__icontains=query)
        else:
            search_results = []

        print("Query:", query)
        print("Search Results:", search_results)

        context = {
            'query': query,
            'search_results': search_results,
        }
        return render(request, self.template_name, context)


class DetailBookView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'  