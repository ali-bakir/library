from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, \
    reverse
from .forms import BookForm, FavouriteBookForm
from .models import Book, Comment, FavouriteBook
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def books(request):
    keyword = request.GET.get("keyword")

    if keyword:
        books = Book.objects.filter(title__contains=keyword)
        return render(request, "books.html", {"books": books})
    books = Book.objects.all()

    return render(request, "books.html", {"books": books})


def index(request):
    return render(request, "index.html", {"number": 7})


def about(request):
    return render(request, "about.html")


@login_required(login_url="user:login")
def dashboard(request):
    books = Book.objects.all()
    context = {"books": books}
    return render(request, "dashboard.html", context=context)


@login_required(login_url="user:login")
def favourite(request):
    favourite_books = FavouriteBook.objects.select_related(
        'book',
        'book__author',
        'user').filter(
        user=request.user)
    print(favourite_books.query)
    context = {"favourite_books": favourite_books}
    return render(request, "favourite.html", context=context)


@login_required(login_url="user:login")
def add_favourite(request, id):
    form = FavouriteBookForm({'user': request.user.id, 'book': id})
    if form.is_valid():
        form.save()
        messages.success(request, "Favorilere eklendi.")

    return render(request, "add_favourite.html")


@login_required(login_url='user:login')
def delete_favourite(request, id):
    print(id)
    pass


@login_required(login_url="user:login")
def wish(request):
    books = Book.objects.all()
    context = {"books": books}
    return render(request, "wish.html", context=context)


@login_required(login_url="user:login")
def add_wish(request, id):
    form = BookForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        book = form.save(commit=True)
        messages.success(request, "İstek Kitaplığına Eklendi")

    return render(request, "add_wish.html", {"form": form})


@login_required(login_url="user:login")
def add_book(request):
    print(request.POST)
    form = BookForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        book = form.save(commit=True)
        messages.success(request, "Kitap Başarıyla Oluşturuldu")

    return render(request, "add_book.html", {"form": form})


@login_required(login_url="user:login")
def updateBook(request, id):
    book = get_object_or_404(Book, id=id)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if form.is_valid():
        book = form.save(commit=True)

        book.author = request.user
        book.save()

        messages.success(request, "Kitap başarıyla güncellendi")
        return redirect("book:dashboard")
    return render(request, "update.html", {"form": form})


def detail(request, id):
    book = Book.objects.filter(id=id).first()
    book = get_object_or_404(Book, id=id)

    comments = book.comments.all()
    return render(request, "detail.html", {"book": book, "comments": comments})


@login_required(login_url="user:login")
def deleteBook(request, id):
    book = get_object_or_404(Book, id=id)

    book.delete()

    messages.success(request, "Kitap Başarıyla Silindi")
    return redirect("book:dashboard")


def comment(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author=comment_author,
                             comment_content=comment_content)

        newComment.book = book

        newComment.save()
    return redirect(reverse("book:detail", kwargs={"id": id}))
