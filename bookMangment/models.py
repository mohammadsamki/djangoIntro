from django.db import models
from django.urls import reverse

# Create your models here.


class Geneger(models.Model):
    ''' this is a model for geneger '''
    name = models.CharField(max_length=100, help_text='gene name')

    def __str__(self):
        '''deafult returns the name of the geneger'''
        return self.name


class Language(models.Model):
    ''' this is a model for Language '''
    name = models.CharField(max_length=100, help_text='gene name')

    def __str__(self):
        '''deafult returns the name of the Language'''
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100, help_text='book title')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, help_text='author', null=True)
    isbn = models.CharField(max_length=100, help_text='ISBN')
    gener = models.ManyToManyField(Geneger, help_text='geneger')
    summery = models.TextField(max_length=1000, help_text='book summ')

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})
    def display_genre(self):
        return ', '.join(self.gener.__str__())
    def __str__(self):
        return self.title


class Author(models.Model):
    firstName = models.CharField(max_length=100, help_text='author name')
    lastName = models.CharField(max_length=100, help_text='author name')
    date_of_birth = models.DateField(help_text='date of birth', null=True)
    date_of_dith = models.DateField(help_text='date of dith' , null=True, blank=True)

    def __str__(self):
        return self.firstName + '' + self.lastName


import uuid  # Required for unique book instances


class BookInstance(models.Model):

    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

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
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
