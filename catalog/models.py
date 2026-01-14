import uuid

from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='Enter genre')
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('genre-detail', srgs=[str(self.id)])
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name = 'genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)" ),
        ]


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    summary = models.TextField(
        max_length=1000,
        help_text='Enter summary of the book',
        null=True,
    )
    isbn = models.CharField('ISBN', max_length=20, unique=True, help_text='<a href="https://www.isbn-international.org/content/what-isbn'
                                      '">Enter ISBN of the book</a>')
    genre = models.ManyToManyField(Genre, blank=True, help_text='Select genre')

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all())
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=100, blank=True, null=True)
    due_back = models.DateField(blank=True, null=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),

    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return self.book.title


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return self.first_name + ' ' + self.last_name
