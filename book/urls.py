from django.urls import path
from . import views
from .views import BookView, FavouriteBookView, DashboardView, WishBookView

app_name = "book"

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    #path('add_book/', views.add_book, name="add_book"),
    path('update/<int:pk>/', views.BookView.as_view(), name="update"),
    path('book/<int:id>', views.detail, name="detail"),
    path('delete/<int:pk>', BookView.as_view(), name="delete"),
    path('', BookView.as_view(), name="books"),
    path('comment/<int:id>', views.comment, name="comment"),
    path('favourite/', FavouriteBookView.as_view(), name="favourite"),
    #path('delete_favourite/<int:pk>', FavouriteBookView.as_view(),
         #name="delete_favourite"),
    path('add_wish/', WishBookView.as_view(), name="add_wish"),
    #path('favourite/', FavouriteBookView.as_view(), name="favourite"),
    path('wish/', WishBookView.as_view(), name="wish"),
    path('delete_wish/<int:pk>', WishBookView.as_view(),
         name="delete_wish"),

]

