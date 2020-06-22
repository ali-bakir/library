from django.urls import path
from . import views
from .views import BookView, FavouriteBookView

app_name = "book"

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    #path('add_book/', views.add_book, name="add_book"),
    path('update/<pk>/', views.BookView.as_view(), name="update"),
    path('book/<int:id>', views.detail, name="detail"),
    path('delete/<int:id>', views.delete_book, name="delete"),
    path('', BookView.as_view(), name="books"),
    path('comment/<int:id>', views.comment, name="comment"),
    path('add_favourite/<pk>', FavouriteBookView.as_view(), name="add_favourite"),
    path('delete_favourite/<pk>', FavouriteBookView.as_view(),
         name="delete_favourite"),
    path('add_wish/', views.add_wish, name="add_wish"),
    path('favourite/', FavouriteBookView.as_view(), name="favourite"),
    path('wish/', views.wish, name="wish"),
    path('delete_wish/<int:id>', views.delete_wish,
         name="delete_wish"),

]

