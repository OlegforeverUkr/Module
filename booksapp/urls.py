from django.urls import path
from . import views

app_name = "booksapp"
urlpatterns = [ 
    path('', views.BookListView.as_view(), name='home_page'),
    path('borrow_history/', views.BorrowListView.as_view(), name='borrow_list'),
    path('borrow_request/<int:pk>/', views.BorrowRequestView.as_view(), name='borrow_request'),
    path('create-book/', views.CreateBookView.as_view(), name='create_book'),
    path('search-results/', views.SearchResultsView.as_view(), name='search_results'),
    path('books/<int:pk>/', views.DetailBookView.as_view(), name='book_detail'),
]