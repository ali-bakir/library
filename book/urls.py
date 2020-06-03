from django.contrib import admin
from django.urls import path
from . import views

app_name = "book"

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('add_book/', views.add_book, name="add_book"),
    path('update/<int:id>', views.updateBook, name="update"),
    path('book/<int:id>', views.detail, name="detail"),
    path('delete/<int:id>', views.deleteBook, name="delete"),
    path('', views.books, name="books"),
    path('comment/<int:id>', views.comment, name="comment"),
    path('add_favourite/<int:id>', views.add_favourite, name="add_favourite"),
    path('delete_favourite/<int:id>', views.delete_favourite,
         name="delete_favourite"),
    path('add_wish/<int:id>', views.add_wish, name="add_wish"),
    path('favourite/', views.favourite, name="favourite"),
    path('wish/', views.wish, name="wish"),

]
