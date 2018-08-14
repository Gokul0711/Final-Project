from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Profiles, Trees
from .helpers import upload_file, get_profile, update_badges

# Create your views here.
def index(request):
    """Index view"""
    return render(request, 'gotrees/index.html')

def register(request):
    """Register view"""
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]


        user = User.objects.create_user(username, email, password, first_name=first_name)
        user.save()
        profile = Profiles.objects.create(user_id=user)
        profile.save()
        badge = Badges.objcts.create(user=user)
        badge.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "gotrees/register.html")

def login_page(request):
    """Login view"""
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "gotrees/login.html", {"message": "Sorry, your username or password is incorrect"})

    else:
        return render(request, "gotrees/login.html")


def logout_page(request):
    """Logout view"""
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def myforest(request, user_username):
    """Public profile view"""
    update_badges(user_username)
    context = get_profile(user_username)
    return render(request, "gotrees/myforest.html", context)


def edit_profile(request, user_username):
    """Editing profile"""
    # Just granting acces to profile owner
    if request.user.username == user_username:
        if request.method == 'POST':
            try:
                file = request.FILES["profile_image"]
                image = upload_file(file, user_username)
            except KeyError:
                image = ''

            name = request.POST["name"]
            my_phrase = request.POST["my_phrase"]
            country = request.POST["country"]
            region = request.POST["region"]
            my_text = request.POST["my_text"]

            user = User.objects.get(id=request.user.id)
            user.first_name = name
            user.save()

            if len(user.profile.all()) == 0:
                profile = Profiles.objects.create(country=country, region=region, my_phrase=my_phrase, my_text=my_text, user_id=user)

                if image == False:
                    profile.save()
                    context = get_profile(user_username)
                    context["message"] = True
                    return render(request, 'gotrees/edit_profile.html', context)
                else:
                    return HttpResponseRedirect(reverse('myforest', kwargs={"user_username": user_username}))
            else:
                Profiles.objects.filter(user_id=user).update(country=country, region=region, my_phrase=my_phrase, my_text=my_text)
                profile = Profiles.objects.get(user_id=user)

                if image == False:
                    context = get_profile(user_username)
                    context["message"] = True
                    return render(request, 'gotrees/edit_profile.html', context)
                else:
                    return HttpResponseRedirect(reverse('myforest', kwargs={"user_username": user_username}))
        else:
            context = get_profile(user_username)
            return render(request, 'gotrees/edit_profile.html', context)
    else:
        return HttpResponseRedirect(reverse('index'))

def new_tree(request, user_username):
    if request.user.username == user_username:
        if request.method == "POST":

            lat = float(request.POST["lat"])
            lng = float(request.POST["lng"])
            tree_name = request.POST["tree_name"]
            tree_kind = request.POST["tree_kind"]
            tree_dedication = request.POST["tree_dedication"]

            user = User.objects.get(username=user_username)
            tree = Trees.objects.create(lat=lat, lng=lng, kind=tree_kind, name=tree_name, dedication=tree_dedication, user=user)

            tree.save()

            return HttpResponseRedirect(reverse('myforest', kwargs={"user_username": user_username}))

        else:
            return render(request, 'gotrees/new_tree.html')
    else:
        return HttpResponseRedirect(reverse('index'))


def add_marker(request):
    """Add one tree-marker to the map"""

    lat = request.POST["lat"]
    lng = request.POST["lng"]

    user = User.objects.get(username=request.user.username)
    marker = Markers.objects.create(lat=lat, lng=lng, user=user)

    marker.save()
    return JsonResponse({"success": True})

def delete_marker(request):
    """Remove a tree-marker from map"""
    id = request.POST["id"]


    tree_to_remove = Trees.objects.get(id=id)
    tree_to_remove.delete()

    return JsonResponse({"success": True})

def add_old_markers(request):
    """Add all already planted tree-markers to map"""

    user_username = request.POST["user_username"]

    user = User.objects.get(username=user_username)
    trees = Trees.objects.filter(user=user).values()

    feed = list(trees)
    return JsonResponse(feed, safe=False)
