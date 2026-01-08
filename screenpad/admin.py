from django.contrib import admin
from .models import Book, Entry, EntryLike, Genre

admin.site.register(Book)
admin.site.register(Entry)
admin.site.register(Genre)
admin.site.register(EntryLike)


# Register your models here.
