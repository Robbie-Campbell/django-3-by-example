from django.test import TestCase
from blog.models import Comment, Post
from django.contrib.auth.models import User


class DatabaseTestCase(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title="title", author=User.objects.create())
        self.comment = Comment.objects.create(post=Post.objects.first(), name="firstname")

    def test_validate_data_in_category(self):
        comm = self.comment
        post = self.post
        self.assertTrue(isinstance(comm, Comment))
        self.assertTrue(str(comm), f"Comment by {self.name} on {self.post}")
        self.assertNotEqual(str(comm), "hello")
        self.assertTrue(isinstance(post, Post))
        self.assertTrue(str(post), "title")
        self.assertNotEqual(str(post), "hello")