from django.urls import path
from . import views


app_name = "usersapp"
urlpatterns = [ 
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('office/', views.OfficeView.as_view(), name='office'),
    path('manage-books/', views.ManageBooksView.as_view(), name='manage_books'),
    path('edit-book/<int:pk>/', views.EditBookView.as_view(), name='edit_book'),
    path('manage-authors/', views.ManageAuthorsView.as_view(), name='manage_authors'),
    path('edit-author/<int:pk>/', views.EditAuthorView.as_view(), name='edit_author'),
    path('create-author/', views.CreateAuthorView.as_view(), name='create_author'),
    path('manage-genres/', views.ManageGenresView.as_view(), name='manage_genres'),
    path('edit-genre/<int:pk>/', views.EditGenreView.as_view(), name='edit_genre'),
    path('create-genre/', views.CreateGenreView.as_view(), name='create_genre'),
    path('manage-requests/', views.ManageBorrowRequestsView.as_view(), name='manage_requests'),
    path('user-office/', views.UserOfficeView.as_view(), name='user_office'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('delete/<int:pk>/', views.DeleteBookView.as_view(), name='delete_book'),
    path('all-requests/<int:user_id>/', views.UserRequestsListView.as_view(), name='user_all_requests'),
]