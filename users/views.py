from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UserUpdateForm,
    UserPasswordChangeForm,
)

# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("profile")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("userposts")
            else:
                messages.error(request, "Invalid username or password")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserLoginForm()
    return render(request, "login.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(
                request, "Your profile information has been updated successfully!"
            )
            return redirect("profile")
        else:
            for errors in user_form.errors.values():
                for error in errors:
                    messages.error(request, error)
            password_form = UserPasswordChangeForm(user=request.user)
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = UserPasswordChangeForm(user=request.user)
    context = {
        "user_form": user_form,
        "password_form": password_form,
        "user": request.user,
    }
    return render(request, "profile.html", context)


@login_required
def user_password_change(request):
    if request.method == "POST":
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # IMPORTANT: After changing password, the user's session is invalidated.
            # This function keeps the user logged in after a password change.
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("profile")  # Redirect to profile or a success page
        else:
            # Display form errors
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error)
    else:
        form = UserPasswordChangeForm(user=request.user)

    return render(request, "changepassword.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")
