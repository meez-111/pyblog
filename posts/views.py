from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.text import slugify
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

from .models import Post, Category
from .forms import ContactForm, PostForm


# Create your views here.
def index(request):
    posts = Post.objects.all().exclude(status="draft")
    return render(request, "index.html", {"posts": posts})


def post(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "post.html", {"post": post})


@login_required
def user_posts(request):
    user_posts = Post.objects.filter(author=request.user).order_by("publish_date")
    return render(request, "userposts.html", {"user_posts": user_posts})


def create_post(request):
    category = Category.objects.all()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user

            new_post.save()

            messages.success(request, "post created successfully")

            return redirect("userposts")
    else:
        form = PostForm()
    return render(
        request,
        "createpost.html",
        {"form": form, "form_type": "Create", "category": category},
    )


def update_post(request, post_id):
    category = Category.objects.all()
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        messages.error(request, "you are not authorized to edit this post")
        return redirect("userposts")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            updated_post = form.save(commit=False)

            updated_post.save()
            return redirect("userposts")
    else:
        form = PostForm(instance=post)

    return render(request, "updatepost.html", {"form": form, "category": category})


@login_required
@require_POST
def delete_post(request, post_id):
    """
    Allows the author of a post to delete it.
    """
    user_post = get_object_or_404(Post, id=post_id)

    # Security check: Ensure the logged-in user is the author of the post
    if user_post.author != request.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect("userposts")  # Redirect if not authorized
    else:
        user_post.delete()
        messages.success(request, "Your post has been deleted successfully!")
        return redirect("userposts")


def about(request):

    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            try:
                # Send the email
                send_mail(
                    subject=f"New Contact from Blog: {name}",
                    message=f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,  # Or a specific email, e.g., 'your_blog_no_reply@example.com'
                    recipient_list=[
                        settings.CONTACT_EMAIL
                    ],  # The email address where you want to receive messages
                    fail_silently=False,  # Set to True to suppress exceptions
                )
                return redirect(
                    "contact"
                )  # Redirect to a success page or the same page with a message
            except Exception as e:
                messages.error(
                    request,
                    f"There was an error sending your message. Please try again later. Error: {e}",
                )
        else:
            form = ContactForm(request.POST)
            messages.error(request, "Please correct the errors below.")

    return render(request, "contact.html", {"form": ContactForm()})
