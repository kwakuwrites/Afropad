from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models import Sum


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    

    def __str__(self):
        return self.name

class Entry(models.Model):
    book = models.ForeignKey('Book', related_name='entries', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(editable=False)
    is_published = models.BooleanField(default=False)
    footprints = models.PositiveIntegerField(default=0)
    entry_id = models.AutoField(primary_key=True)
    visitors  = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name = 'visited_entries')
    

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.pk:
            last_entry = Entry.objects.filter(book=self.book).order_by('-order').first()
            self.order = last_entry.order + 1 if last_entry else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class EntryLike(models.Model):
    entry = models.ForeignKey(Entry, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='entry_likes', on_delete=models.CASCADE)
   

    class Meta:
        unique_together = ('entry', 'user')



# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    genre = models.ForeignKey(Genre, related_name="books", on_delete=models.CASCADE, null=True)
    published_date = models.DateField(auto_now_add=True)
    book_description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='books', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    cover_image = models.ImageField( upload_to='book_covers/', default='book_covers/default_cover.png', blank=True, null=True)
    
    def total_footprints(self):
        return self.entries.aggregate(total=Sum('footprints'))['total'] or 0
    
   
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while Book.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
  


class Comment(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"