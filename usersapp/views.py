from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import FormView, ListView, TemplateView, UpdateView, CreateView, DeleteView
from .forms import RegistrationForm, CreateAuthorForm, CreateGenreForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth import logout
from booksapp.models import Book, Author, Genre, BorrowRequest, UserModel, Message
from booksapp.forms import CreateBookForm


class UserLoginView(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('booksapp:home_page')

class UserRegistrationView(FormView):
    http_method_names = ['get', 'post']
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('usersapp:login')

    def form_valid(self, form):
        form.create_user()
        return redirect(self.success_url)

class UserLogoutView(LogoutView):
    def get(self, request):
        logout(request)
        return redirect('usersapp:login')


class OfficeView(TemplateView):
    template_name = 'office.html'


class ManageBooksView(ListView):
    model = Book
    template_name = 'manage_book.html'
    context_object_name = 'books'

    def post(self, request):
        book_id = request.POST.get('book_id')
        action = request.POST.get('action')

        if action == 'edit':
            return redirect(reverse_lazy('usersapp:edit_book', kwargs={'pk': book_id}))
        
        return redirect(reverse_lazy('usersapp:manage_books'))


class EditBookView(UpdateView):
    model = Book
    form_class = CreateBookForm
    template_name = 'edit_book.html'
    success_url = reverse_lazy('usersapp:manage_books')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs


class ManageAuthorsView(ListView):
    model = Author
    template_name = 'manage_authors.html'
    context_object_name = 'authors'

    def post(self, request):
        author_id = request.POST.get('author_id')
        action = request.POST.get('action')

        if action == 'edit':
            return redirect(reverse_lazy('usersapp:edit_author', kwargs={'pk': author_id}))
        elif action == 'delete':
            try:
                author = Author.objects.get(pk=author_id)
                author.delete()
            except Author.DoesNotExist:
                raise Author.DoesNotExist('This author is not found')
        
        return redirect(reverse_lazy('usersapp:manage_authors'))


class EditAuthorView(UpdateView):
    model = Author
    fields = ['name_author', 'bio_author']
    template_name = 'edit_authors.html'
    success_url = reverse_lazy('usersapp:manage_authors')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs


class CreateAuthorView(CreateView):
    model = Author
    form_class = CreateAuthorForm
    template_name = 'create_author.html'
    success_url = reverse_lazy('usersapp:manage_authors')



class ManageGenresView(ListView):
    model = Genre
    template_name = 'manage_genres.html'
    context_object_name = 'genres'

    def post(self, request):
        genre_id = request.POST.get('genre_id')
        action = request.POST.get('action')

        if action == 'edit':
            return redirect(reverse_lazy('usersapp:edit_genre', kwargs={'pk': genre_id}))
        elif action == 'delete':
            try:
                genre = Genre.objects.get(pk=genre_id)
                genre.delete()
            except Genre.DoesNotExist:
                raise Genre.DoesNotExist('This genre is not found')
        
        return redirect(reverse_lazy('usersapp:manage_genres'))


class EditGenreView(UpdateView):
    model = Genre
    fields = ['name_genre']
    template_name = 'edit_genre.html'
    success_url = reverse_lazy('usersapp:manage_genres')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs


class CreateGenreView(CreateView):
    model = Genre
    form_class = CreateGenreForm
    template_name = 'create_genre.html'
    success_url = reverse_lazy('usersapp:manage_genres')


class ManageBorrowRequestsView(ListView):
    model = BorrowRequest
    template_name = 'manage_borrow_requests.html'
    context_object_name = 'borrow_requests'

    def get_queryset(self):
        return BorrowRequest.objects.order_by('status', 'request_date')


    def post(self, request):
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        if action == 'approve':
            try:
                borrow_request = BorrowRequest.objects.get(pk=request_id)
                borrow_request.status = 2
                borrow_request.save()
            except BorrowRequest.DoesNotExist:
                raise BorrowRequest.DoesNotExist('This request is not found')
        elif action == 'decline':
            try:
                borrow_request = BorrowRequest.objects.get(pk=request_id)
                borrow_request.status = 5
                borrow_request.save()
            except BorrowRequest.DoesNotExist:
                raise BorrowRequest.DoesNotExist('This request is not found')
        elif action == 'delete':
            try:
                borrow_request = BorrowRequest.objects.get(pk=request_id)
                borrow_request.delete()
            except BorrowRequest.DoesNotExist:
                raise BorrowRequest.DoesNotExist('This request is not found')
        elif action == 'change_availability':
            try:
                book_id = request.POST.get('book_id')
                book = Book.objects.get(pk=book_id)
                book.is_available = not book.is_available
                book.save()
            except Book.DoesNotExist:
                raise Book.DoesNotExist('This book is not found')
        elif action == 'send_message':
            request_id = request.POST.get('request_id')
            message_content = request.POST.get('message_content')

            borrow_request = get_object_or_404(BorrowRequest, pk=request_id)

            new_message = Message.objects.create(sender=request.user, content=message_content)
            borrow_request.messages.add(new_message)

        return redirect(reverse_lazy('usersapp:manage_requests'))



class UserOfficeView(ListView):
    model = BorrowRequest
    template_name = 'user_cabinet.html'
    context_object_name = 'borrow_requests'

    def get_queryset(self):
        user = self.request.user
        now = timezone.now().date()

        BorrowRequest.objects.filter(borrower=user, status__in=[1, 2], due_date__lt=now, overdue=False).update(overdue=True)

        return BorrowRequest.objects.filter(borrower=user)
    

    def post(self, request):
        request_id = request.POST.get('request_id')
        message_content = request.POST.get('message_content')

        borrow_request = get_object_or_404(BorrowRequest, pk=request_id)

        new_message = Message.objects.create(sender=request.user, content=message_content)
        borrow_request.messages.add(new_message)
        return redirect('usersapp:user_office')



class ChangePasswordView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('usersapp:login') 


class DeleteBookView(DeleteView):
    model = Book
    template_name = 'book_delete.html'
    success_url = reverse_lazy('booksapp:home_page')


class UserRequestsListView(ListView):
    model = BorrowRequest
    template_name = 'user_all_requests.html'
    context_object_name = 'user_requests'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        user = UserModel.objects.get(pk=user_id)
        context['username'] = user.username
        return context

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return BorrowRequest.objects.filter(borrower_id=user_id)