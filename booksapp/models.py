from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class Author(models.Model):
    name_author = models.CharField(max_length=255, unique=True)
    bio_author = models.TextField()

    class Meta:
        ordering = ['name_author']

    def __str__(self):
        return self.name_author



class Genre(models.Model):
    name_genre = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name_genre



class Book(models.Model):
    book_title = models.CharField(max_length=255)
    book_summary = models.TextField()
    isbn = models.CharField(unique=True)
    is_available = models.BooleanField(default=True)
    published_date = models.DateField()
    publisher_book = models.CharField(max_length=255)

    book_authors = models.ManyToManyField(Author)
    book_genre = models.ManyToManyField(Genre, blank=True)
    book_borrower = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['book_title']

    def __str__(self):
        return self.book_title



class Message(models.Model):
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField()
    time_send = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"From {self.sender} at {self.time_send}"



class BorrowRequest(models.Model):
    overdue = models.BooleanField(default=False)
    request_date = models.DateField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    complete_date = models.DateField(null=True, blank=True)

    STATUS_CHOICES = (
        (1, 'PENDING'),
        (2, 'APPROVED'),
        (3, 'COLLECTED'),
        (4, 'COMPLETE'),
        (5, 'DECLINED'),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_requests')
    borrower = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return f"{self.borrower} - {self.book}"
