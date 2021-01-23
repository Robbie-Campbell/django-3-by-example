from django.contrib import admin
from .models import Post, Comment

# Register your models here.

# Create a specific admin view
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    # What is displayed to the admin for each post
    list_display = ('title', 'slug', 'author', 'publish', 'status')

    # Options to filter the posts by
    list_filter = ('status', 'created', 'publish', 'author')

    # Search for posts by these columns
    search_fields = ('title', 'body')

    # automatically fills in a slug on a new post for us
    prepopulated_fields = {'slug': ('title',)}

    # Search for the user specifically not by a combobox
    raw_id_fields = ('author',)

    # Order by date
    date_heirarchy = 'publish'

    # Order by status first then publish date
    ordering = ('status', 'publish')


# Create a specific admin Comment view
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    # Display the comments in this order
    list_display = ('name', 'email', 'post', 'created', 'active')

    # Allow the admin to narrow down search results
    list_filter = ('active', 'created', 'updated')

    # Search for the different posts based on these values
    search_fields = ('name', 'email', 'body')