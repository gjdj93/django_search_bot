from ast import Pass
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
)
from django.core.exceptions import PermissionDenied
from searches.models import Search
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from .services import send_register_email

# Create your views here.
def index(request):
    context = {}
    if request.user.is_superuser:
        context["users"] = User.objects.filter(is_superuser=False)
        return render(request, "users/index.html", context=context)
    searches = Search.objects.filter(user=request.user)
    context["searches"] = searches
    return render(request, "users/profile.html", context=context)


def view(request, pk):
    if not request.user.is_superuser:
        raise PermissionDenied

    u = get_object_or_404(User, pk=pk)

    return render(request, "users/view.html", context={"user": u})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            send_register_email(user)
            return redirect("users:index")
        messages.error(request, "Registration invalid.")
    form = NewUserForm()
    return render(
        request=request,
        template_name="users/register.html",
        context={"register_form": form},
    )


def login_request(request):
    if request.user.is_authenticated:
        return redirect("users:index")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in as {username}.")
                return redirect("users:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
        print(form.errors)
    form = AuthenticationForm()
    return render(
        request, template_name="users/login.html", context={"login_form": form}
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")


class UserUpdate(UpdateView):
    model = User
    fields = ("username", "email", "first_name", "last_name")

    template_name = "users/edit.html"
    success_url = "/users/"


def user_change_pass(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("users:change_password")
    form = PasswordChangeForm(request.user)
    return render(
        request=request,
        template_name="users/change_password.html",
        context={"form": form},
    )


def user_reset_pass(request):
    form = PasswordResetForm()
    return render(
        request=request,
        template_name="users/reset_password.html",
        context={"form": form},
    )
