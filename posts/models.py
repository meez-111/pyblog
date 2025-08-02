from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    image = models.ImageField(upload_to="images/posts/")
    title = models.CharField(max_length=60)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    publish_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=1000000)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["publish_date"]
        indexes = [
            models.Index(fields=["publish_date"]),
        ]
