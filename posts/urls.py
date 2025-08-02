from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("post/<int:post_id>", views.post, name="post"),
    path("userposts", views.user_posts, name="userposts"),
    path("createpost", views.create_post, name="createpost"),
    path("edit/<int:post_id>", views.update_post, name="updatepost"),
    path("delete/<int:post_id>", views.delete_post, name="deletepost"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
]
