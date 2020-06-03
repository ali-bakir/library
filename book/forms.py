from django import forms
from .models import Book, FavouriteBook


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'content', "book_image"]


form = BookForm()


class FavouriteBookForm(forms.ModelForm):
    class Meta:
        model = FavouriteBook
        fields = ['user', 'book']
