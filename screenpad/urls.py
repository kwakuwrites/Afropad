from django.urls import path
from . import views
from .views import create_a_book
from .views import book_entries
from .views import new_entry
from .views import book_list 


app_name = 'screenpad'
urlpatterns = [
    path('', views.index, name='index'),
    path("genres/<int:pk>/", views.genre_detail, name="genre_detail"),
    path("books/<slug:book_slug>/", views.book_detail, name="book_detail"),
    path("books/<slug:book_slug>/entries/<int:order>/", views.entry_detail, name="entry_detail"),
    path("create_a_book/", views.create_a_book, name="create_a_book"),
    path("books/<slug:book_slug>/entries/", views.book_entries, name="book_entries"),
    path("create_another_book/", views.create_another_book, name="create_another_book"),
    path("edit_entry/<int:pk>/", views.edit_entry, name="edit_entry"),
    path("books/<slug:book_slug>/entries/new/", views.new_entry, name="new_entry"),
    path("new_entry/", views.new_entry, name="new_entry"),
    path("books/<slug:book_slug>/read/<int:order>/", views.read_entry, name="read_entry"),
    path("books/<slug:book_slug>/like/<int:order>/toggle_like/", views.toggle_like, name="toggle_like"),
    path("books/<slug:book_slug>/read/<int:order>/screenpad/read_entry/", views.read_entry, name="read_entry"),
    path("books/", views.book_list, name="book_list")
]
