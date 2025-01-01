from django.shortcuts import render, redirect
from publice.models import *
from .forms import *
from users.auth import admin_only
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
@admin_only
def admin_dashboard(request):
    return render(request, 'admins/index.html')

# def amenities_list(request):
#     amenities = Amenities.objects.all()
#     context = {"amenities": amenities}
#     return render(request, "admins/amenities_list.html", context)

# def add_amenities(request):
#     form = AmenitiesForm(request.POST, request.FILES)
#     if form.is_valid():
#         form.save()
#         return redirect("/amenities_list")
#     else:
#         form = AmenitiesForm()
#         return render(request, "admins/amenities_form.html", {"form": form})

# def amenities_delete(request, pk):
#     amenities = Amenities.objects.all()
#     if request.method == "Post":
#         amenities.delete()
#         return redirect("/amenities_list")
#     return render(request, "admins/amenities_delete.html", {"amenities": amenities})


# @login_required
# @admin_only
# def index(request):

#     # Page from the theme 
#     return render(request, 'pages/index.html')