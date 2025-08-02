from django import forms
from .models import Post, Category
from django.core.exceptions import ValidationError


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Name", "class": "form-name"}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-email"}),
    )
    subject = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Subject", "class": "form-subject"}
        ),
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "Message", "rows": 5, "class": "form-message"}
        ),
    )


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category",
        required=False,
    )

    class Meta:
        model = Post
        fields = ["title", "content", "category", "status", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter post title", "class": "post-title"}
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Write your post content here...",
                    "rows": 15,
                    "class": "post-content",
                }
            ),
            "category": forms.Select(attrs={"class": "post-category"}),
            "status": forms.Select(attrs={"class": "post-status"}),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "post-image",
                    "accept": "image/*",
                }
            ),
        }

    def clean_post_image(self):

        image = self.cleaned_data_get("image")

        if image:

            max_size = 2 * 1024 * 1024

            if image.size() > max_size:

                raise ValidationError

        return image
