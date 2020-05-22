from django.contrib import admin

from .models import Book, Author, Publisher


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_date", "content"]
    list_display_links = ["title", "created_date"]
    search_fields = ["title", "author", "content"]
    list_filter = ["created_date"]

    class Meta:
        model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "last_name", "birthday"]
    list_display_links = ["name", "last_name", "birthday"]
    search_fields = ["name", "last_name", "birthday"]
    list_filter = ["name", "last_name", "birthday"]

    class Meta:
        model = Author


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]

    class Meta:
        model = Publisher
