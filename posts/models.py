from django.db import models
from datetime import datetime


# Create your models here.
class Post(models.Model):
    image = models.ImageField(upload_to="images/posts/")
    title = models.CharField(max_length=60)
    publish_date = models.DateTimeField(default=datetime.now, blank=True)
    content = models.TextField(max_length=1000000)
