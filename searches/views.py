from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import UpdateView
from django.contrib import messages
from .forms import SearchForm
from .models import Search
from django.utils import timezone

# Create your views here.
def index(request):
    pass


def create(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.save(commit=False)
            search.user = request.user
            search.save()
            messages.success(
                request,
                "Search item added, we will let you know if we find your item in stock!",
            )
            return redirect("users:index")
        messages.error(request, "Invalid form")
    form = SearchForm()
    return render(
        request,
        template_name="searches/form.html",
        context={"form": form, "form_type": "New"},
    )


def view(request, pk):
    search = get_object_or_404(Search, pk=pk)
    if not request.user.is_superuser and search.user != request.user:
        raise PermissionDenied

    return render(
        request, template_name="searches/view.html", context={"search": search}
    )


class SearchUpdate(UpdateView):
    model = Search
    fields = ("name", "url", "phrase", "found")

    template_name = "searches/form.html"
    success_url = "/users"


def delete(request, pk):
    search = get_object_or_404(Search, pk=pk)
    if not request.user.is_superuser and search.user != request.user:
        raise PermissionDenied

    search.delete()
    if "next" in request.GET:
        return redirect(request.GET["next"])


def found(request, pk):
    search = get_object_or_404(Search, pk=pk)
    if not request.user.is_superuser and search.user != request.user:
        raise PermissionDenied

    search.found = True
    search.date_found = timezone.now()
    if "next" in request.GET:
        return redirect(request.GET["next"])
    return redirect("users:index")
