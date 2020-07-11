from django import forms
from .models import Book, FavouriteBook, WishBook, WishAuthor, WishPublisher, \
    Comment


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'content', "book_image"]


class FavouriteBookForm(forms.ModelForm):
    class Meta:
        model = FavouriteBook
        fields = ['user', 'book']


class WishAuthorForm(forms.ModelForm):
    class Meta:
        model = WishAuthor
        fields = "__all__"


class WishPublisherForm(forms.ModelForm):
    class Meta:
        model = WishPublisher
        fields = "__all__"


class WishBookForm(forms.ModelForm):
    class Meta:
        model = WishBook
        fields = ['title', 'author', 'publisher']

    def __init__(self, *args, **kwargs):
        super(WishBookForm, self).__init__(*args, **kwargs)
        self.fields['author'].widget = forms.TextInput()
        self.fields['publisher'].widget = forms.TextInput()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
