from django.test import TestCase
from blog.models import Comment, Post
from django.contrib.auth.models import User
import datetime


class DatabaseTestCase(TestCase):

    # Create objects for testing
    def setUp(self):
        self.post = Post.objects.create(title="title", author=User.objects.create_user('foo', 'myemail@test.com', 'bar'), created = datetime.datetime(2021, 1, 22, 13, 41, 34, 963630), slug="title")
        self.comment = Comment.objects.create( name="hello", post=Post.objects.first())

    # Test the post model
    def test_validation_in_post(self):

        # Create testing variable
        post = self.post

        # Tests
        self.assertTrue(isinstance(post, Post)) # Test: is this a post object
        self.assertTrue(str(post), "title") # Test: is the return value correct
        self.assertNotEqual(str(post), "hello") # Test: is the return value correct

    # Test the comment model
    def test_validation_in_comment(self):

        # Create testing variable
        comm = self.comment

        # Tests
        self.assertTrue(isinstance(comm, Comment)) # Test: is this a comment object
        self.assertTrue(str(comm), f"Comment by {comm.name} on {comm.post}") # Test: is the return value correct
        self.assertNotEqual(str(comm), "hello") # Test: is the return value correct

    # Make sure that the url is correct
    def test_absolute_url(self):
        
        # Create testing variable
        post = self.post
        
        # Test
        self.assertEqual(post.get_absolute_url(), "/blog/%d/%d/%d/%s/" % (int(post.created.strftime('%Y')), int(post.created.strftime('%m')), int(post.created.strftime('%d')), post.slug)) # Make sure the url is correct

