from urllib import request
from django.shortcuts import render, redirect
from .models import EntryLike, Genre
from .models import Comment
from django.shortcuts import get_object_or_404
from .models import Book
from .models import Entry
from .forms import BookForm, EntryForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import F, ExpressionWrapper, FloatField 
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count
from django.urls import reverse 



def index(request):
    genres = Genre.objects.all()
    return render(request, 'screenpad/index.html', {'genres': genres})

def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    books = Book.objects.filter(genre=genre).annotate(total_likes=Count('entries__likes', distinct=True),
    total_footprints = Count('entries__footprints', distinct=True), 
    total_comments = Count('entries__comments', distinct=True)).annotate(score = ExpressionWrapper(
        F('total_likes')*3 +
        F('total_footprints')*1 +
        F('total_comments')*2,
        output_field = FloatField()
    )).order_by('-score')
    for book in books :
        print(book.title, book.total_likes)
    
    
    return render(request, 'screenpad/genre_detail.html', { 'genre': genre, 'books': books})

def book_detail(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    entries = book.entries.all()
    
    return render(request, 'screenpad/book_detail.html', {'book': book, 'entries': entries})
    
@login_required
def entry_detail(request, book_slug, order):
    book = get_object_or_404(Book, slug=book_slug)
    entry = get_object_or_404(book.entries.all(), order=order)
    book_slug = book.slug
    return render(request, 'screenpad/entry_detail.html', {'book': book, 'entry': entry, 'book_slug': book_slug })

def read_entry(request, book_slug, order):
    book = get_object_or_404(Book, slug=book_slug)
    entry = get_object_or_404(book.entries.all(), order=order )
    
    if request.user.is_authenticated and request.user not in entry.visitors.all():
        entry.visitors.add(request.user)
        entry.footprints = entry.visitors.count()
        entry.save()
    book_slug = book.slug
    like_count = entry.likes.count()
    comments = entry.comments.all()
    
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.entry = entry 
                comment.user = request.user 
                comment.save()
            redirect('read_entry.html', slug=book_slug, order=entry.order)
        else:
            return redirect('login')
    else:
        form = CommentForm(prefix='comment')
    return render(request, 'screenpad/read_entry.html', {'book': book, 'entry': entry , 'comments': comments, 'form': form, 'book_slug': book_slug , 'like_count': like_count})

@require_POST
def toggle_like(request, book_slug, order):
    print("LIKE VIEW HIT")
    book = get_object_or_404(Book, slug=book_slug)
    entry = get_object_or_404(Entry, book__slug=book_slug, order=order)
    like = EntryLike.objects.filter(entry=entry, user =request.user).first()
    if not request.user.is_authenticated:
        return JsonResponse({'error':'login required'}, status=403)
    
    if like:
        
        liked = False
    else:
        EntryLike.objects.create(entry=entry, user=request.user)
        liked = True
    likes_count = EntryLike.objects.filter(entry=entry).count()
   
    return JsonResponse({'liked': liked, 'likes_count': likes_count})

@login_required    
def edit_entry(request, pk):
    entry = Entry.objects.get(entry_id=pk)
    title = entry.title
    if request.method != "POST":
        print("GET request to edit entry")
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('screenpad:book_entries', book_slug=entry.book.slug)
            
    return render(request, 'screenpad/edit_entry.html', {'entry': entry, 'title': title, 'form': form})

def book_list(request): 
    books = Book.objects.filter(owner=request.user)
    return render(request, "screenpad/book_list.html", {"books": books})


@login_required
def create_another_book(request):
    if request.method == "POST":
        book_form = BookForm(request.POST, request.FILES)
        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.owner = request.user
            book.save()
            print(f"Book created: {book.title}")
            return redirect(reverse("screenpad:book_list"))
        
    else :
            book_form = BookForm()
            
    return render(request, 'screenpad/create_another_book.html' ,{'book_form': book_form})



@login_required
def create_a_book(request):
    print("create_a_book view called")
    books = Book.objects.filter(owner=request.user)
    print(f"Books found: {books.count()}")
    if not books.exists():
        print("no books found for user")
        if request.method == "POST":
            print("post request received")
            book_form = BookForm(request.POST, request.FILES)
            if book_form.is_valid():
                book = book_form.save(commit=False)
                book.owner = request.user
                book.save()
                print(f"Book created: {book.title}")
                return redirect('screenpad:create_a_book' )
    
        else:
            print("get request received")
            book_form = BookForm()
        return render(request, 'screenpad/book_list.html', {'book_form': book_form})
    
    return render(request, 'screenpad/book_list.html', {'books': books,})
    
@login_required
def book_entries(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug, owner=request.user)
    selected_book = None
    entry_form = None
    if book_slug is not None:
        selected_book = book
        print(f"Selected book: {selected_book.title}")
        entry = selected_book.entries.all()
    return render(request, 'screenpad/entry_detail.html', { 'selected_book': selected_book, 'entry': entry})


@login_required
def new_entry(request, book_slug):
    print("new_entry view called")
    book = get_object_or_404(Book, slug=book_slug, owner=request.user)
    if request.method == "POST":
        print("POST request for adding entry received")
        entry_form = EntryForm(request.POST)
        print(f"Entry form requested")
        if entry_form.is_valid():
            entry = entry_form.save(commit=False)
            entry.book = book
            entry.save()
            return redirect('screenpad:book_entries', book_slug=book.slug)
        
    else:
        entry_form = EntryForm()
        print("GET request for adding entry received")
        return render(request, 'screenpad/entries.html', {'book':book, 'entry_form': entry_form})
        
    return render(request, 'screenpad/entry_detail.html', {'book': book, 'entry_form': entry_form})


