from django import forms
from .models import Book, Entry, Comment

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['cover_image', 'title', 'author', 'genre', 'book_description']
        widgets = { 'title': forms.TextInput(attrs={'placeholder':'Title', 'class':'book-title'}),
                    'genre' : forms.Select(attrs={'class':'book-genre','placeholder': 'Genre'}),
                    'book_description' : forms.Textarea(attrs={'class':'book-description','placeholder': 'Book Description'}),
                    'author' : forms.TextInput(attrs={'class':'book-author','placeholder': 'Author'}),
                    'cover_image' : forms.ClearableFileInput(attrs={'class':'book-cover-image','placeholder': 'Book Cover'})
                }
        labels ={ 'title':'', 'author':'', 'genre':'', 'book_description':''}
                
                  
                    

                                                   


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'content']
        widgets = {'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'entry-title'}),
                   'content': forms.Textarea(attrs={'placeholder': 'Enter your story', 'class': 'entry-content'})
                    }
        labels ={ 'title':'', 'content':''}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [ 'content']
        widgets = {
                   'content': forms.Textarea(attrs={'placeholder': 'Voices', 'rows':3, 'class': 'comment-input'})
                    }
    
