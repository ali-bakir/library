from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, \
    reverse
from .forms import BookForm, FavouriteBookForm, WishBookForm, WishAuthorForm, \
    WishPublisherForm, CommentForm
from .models import Book, Comment, FavouriteBook, WishBook
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView, CreateView, \
    UpdateView, DeleteView, TemplateView


class BookView(View):
    form_class = BookForm
    template_name = "books.html"
    queryset = Book.objects.all()

    def dispatch(self, request, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(request, *args, **kwargs)
        if method == 'delete':
            return self.delete(request, *args, **kwargs)
        return super(BookView, self).dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(request, *args, **kwargs)
        if method == 'delete':
            return self.delete(request, *args, **kwargs)
        return super(FavouriteBookView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        favourite_books = FavouriteBook.objects.select_related(
            'book',
            'book__author',
            'user').filter(
            user=request.user)

        context = {"favourite_books": favourite_books}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
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
        print('33333')
        fav_id = data.get('fav_id', None)
        FavouriteBook.objects.filter(id=fav_id).delete()

        messages.success(request, "Kaldırıldı.")

        return redirect(reverse("book:favourite"))


class WishBookView(View):
    form_class = WishBookForm
    template_name = 'wish.html'

    def dispatch(self, request, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(request, *args, **kwargs)
        if method == 'delete':
            return self.delete(request, *args, **kwargs)
        return super(WishBookView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        books = WishBook.objects.all()

        return render(request, self.template_name, {"wish": books})

    def post(self, request, *args, **kwargs):
        wish_book_form = WishBookForm(request.POST)
        wish_author_form = WishAuthorForm(request.POST)
        wish_publisher_form = WishPublisherForm(request.POST)
        if wish_book_form.is_valid() and wish_author_form.is_valid() and wish_publisher_form.is_valid():
            wish_publisher_form.save()
            wish_author_form.save()
            wish_book_form.save()
            messages.success(request, "İstek Alındı.")

        return render(request, self.template_name,
                      {"wish_book_form": wish_book_form,
                       "wish_author_form": wish_author_form,
                       "wish_publisher_form": wish_publisher_form})

    def delete(self, request, *args, **kwargs):
        # request.??

        # WishBook.objects.filter(id=id).delete()

        # messages.success(request, "İstek Kitap Kaldırıldı.")

        return redirect(reverse("book:wish"))


class DetailView(View):
    template_name = 'detail.html'

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('pk')
        book = get_object_or_404(Book, id=book_id)
        comments = book.comments.all()
        return render(request, self.template_name,
                      {"book": book, "comments": comments})

    # def post(self, request, *args, **kwargs):
    # book = Book.objects.filter(id=id).first()
    # book = get_object_or_404(Book, id=id)
    # comments = book.comments.all()
    # return render(request, self.template_name,
    # {"book": book, "comments": comments})


class CommentView(View):
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        data = request.POST
        book_id = data.get('book', None)
        book = get_object_or_404(Book, id=book_id)
        is_book_exist = Book.objects.filter(id=book_id).exists()
        form = self.form_class(data)

        if form.is_valid() and is_book_exist:
            data = dict(data)
            data.pop('book', None)
            data.pop('csrfmiddlewaretoken', None)
            Comment.objects.create(book_id=book_id, **data)
            messages.success(request, "Yorum Yayınlandı.")

        return redirect(reverse("book:detail", kwargs={"pk": book_id}))
