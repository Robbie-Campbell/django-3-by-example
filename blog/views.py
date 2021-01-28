from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from blog.models import Post

# Return the view to search for an article by a search form
def post_search(request):

    # Create the default form and create the standard pointers
    form = SearchForm()
    query = None
    results = []

    # If there is a query
    if 'query' in request.GET:

        # Get the query
        form = SearchForm(request.GET)

        # Make sure the data is usable
        if form.is_valid():

            # Format the data
            query = form.cleaned_data['query']

            # Prioritise values which contain the query as a title over a body
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')

            # Run the search
            search_query = SearchQuery(query)

            # Return the results
            results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query).filter(rank__gte=0.3)).order_by('-rank')

    # Render the view
    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
            post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
            f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com',
            [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

# Get all of the posts for the page but paginate into 3 per page
def post_list(request, tag_slug=None):

    # Get all of the posts
    object_list = Post.published.all()
    tag = None

    # Chweck if there are any tags on the post
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)

        # If tags exist, add this value to the post list
        object_list = object_list.filter(tags__in=[tag])

    # Paginate by 3
    paginator = Paginator(object_list, 3)

    # Get the page
    page = request.GET.get('page')

    # Return values for the number of posts in all objects
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})

# Return a single post view
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)

    # List the current comments
    comments = post.comments.filter(active=True)
    new_comment = None

    # Give the option to post a comment on a given post
    if request.method == "POST":

        # If it is valid save the comment to the database and reveal it on the detail page
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    
    # Show the comment form
    else:
        comment_form = CommentForm()

    # Get the tags of the given post and then look for posts which contain the same tags
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)

    # Limit the number of posts to 4 only
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    # Return the view
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'similar_posts': similar_posts})


# Class based version of pagination
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'