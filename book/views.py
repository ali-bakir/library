from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, \
    reverse
from .forms import BookForm, FavouriteBookForm, WishBookForm, WishAuthorForm, \
    WishPublisherForm
from .models import Book, Comment, FavouriteBook, WishBook
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView, CreateView, \
    UpdateView, DeleteView, TemplateView


class BookView(View):
    form_class = BookForm
    template_name = "books.html"
    queryset = Book.objects.all()

    def get_queryset(self, request):
        # self.queryset = self.queryset.filter(user=request.user)
        pass

    def get(self, request, *args, **kwargs):
        self.get_queryset(request)
        keyword = request.GET.get("keyword")
        print(keyword)
        if keyword:
            self.queryset = self.queryset.filter(title__contains=keyword)

        return render(request, self.template_name, {"books": self.queryset})

    def post(self, request, *args, **kwargs):
        self.get_queryset(request)
        # book = get_object_or_404(Book, id=id)
        form = self.form_class(request.POST or None, request.FILES or None)
        if form.is_valid():
            book = form.save(commit=True)
            messages.success(request, "Kitap Başarıyla Oluşturuldu")
        return render(request, self.template_name,
                      {"form": form})

    def delete(self, request, *args, **kwargs):
        queryset = Book.objects.all()
        book = get_object_or_404(Book, pk=pk)

        book.delete()

        messages.success(request, "Kitap Başarıyla Silindi")
        return redirect("book:dashboard")

    def get_context_data(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Book'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("book:dashboard", kwargs={
            'pk': form.instance.pk
        }))


class IndexView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"number": 7})


class AboutView(View):
    template_name = "about.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class DashboardView(View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        context = {"books": books}
        return render(request, self.template_name, context=context)


class FavouriteBookView(View):
    form_class = FavouriteBookForm
    template_name = "favourite.html"
    queryset = FavouriteBook.objects.select_related()
    success_url = '/book'
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        favourite_books = FavouriteBook.objects.select_related(
            'book',
            'book__author',
            'user').filter(
            user=request.user)

        context = {"favourite_books": favourite_books}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        print('22222')
        data = request.POST
        book_id = data.get('book_id', None)
        form = self.form_class({'user': request.user.pk, 'book': book_id})
        if form.is_valid():
            # TODO: check already existence for favourite book
            form.save()
            messages.success(request, "Favorilerine Eklendi.")

        return redirect(reverse("book:favourite"))

    def delete(self, request, *args, **kwargs):
        data = request.POST
        print(data)
        fav_id = data.get('fav_id', None)
        FavouriteBook.objects.filter(id=fav_id).delete()

        messages.success(request, "Kaldırıldı.")

        return redirect(reverse("book:favourite"))


class WishBookView(View):
    form_class = WishBookForm
    template_name = 'wish.html'

    def get(self, request, *args, **kwargs):
        books = WishBook.objects.all()

        return render(request, self.template_name, {"wish": books})

    def post(self, request, *args, **kwargs):
        form = WishBookForm(request.POST)
        form2 = WishAuthorForm(request.POST)
        form3 = WishPublisherForm(request.POST)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            form3.save()
            form2.save()
            form.save()
            messages.success(request, "İstek Alındı.")

        return render(request, self.template_name,
                      {"form": form, "form2": form2, "form3": form3})

    def delete(self, request, *args, **kwargs):
        WishBook.objects.filter(pk=pk).delete()

        messages.success(request, "İstek Kitap Kaldırıldı.")

        return redirect(reverse("book:wish"))


def detail(request, id):
    book = Book.objects.filter(id=id).first()
    book = get_object_or_404(Book, id=id)

    comments = book.comments.all()
    return render(request, "detail.html", {"book": book, "comments": comments})


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
