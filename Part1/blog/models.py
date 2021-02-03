from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# A class that only returns objects which have been published
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

# Create a post class
class Post(models.Model):

    # Make the url for the view based on the values in the database
    def get_absolute_url(self):
        return reverse('blog:post_detail', args = [self.publish.year, self.publish.month, self.publish.day, self.slug])

    # The 2 values that a post can be
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    # Standard values in the database
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # Define the possible object types
    objects = models.Manager()
    published = PublishedManager()

    # Create the tags for a post
    tags = TaggableManager()

    # Order the post on the newest post descending
    class Meta:
        ordering = ('-publish',)

    # Return this value
    def __str__(self):
        return self.title

# Create the comment model
class Comment(models.Model):

    # Standard values in the database
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    # Order by date created
    class Meta:
        ordering = ('created',)

    # The return value
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

