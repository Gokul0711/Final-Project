from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Profiles, Trees
from .helpers import upload_file, get_profile

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
