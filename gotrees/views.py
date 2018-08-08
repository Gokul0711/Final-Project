from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Profiles, Trees

# Create your views here.
def index(request):
    return render(request, 'gotrees/index.html')

def register(request):

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

    logout(request)
    return HttpResponseRedirect(reverse('index'))


def myforest(request, user_username):

    user = User.objects.get(username=user_username)

    context = {
    "user_username": user_username,
    "first_name": user.first_name,
    "country": user.profile.all()[0].country,
    "region": user.profile.all()[0].region,
    "my_phrase": user.profile.all()[0].my_phrase,
    "my_text": user.profile.all()[0].my_text
    }
    return render(request, "gotrees/myforest.html", context)


def edit_profile(request, user_username):


    if request.user.username == user_username:
        if request.method == 'POST':
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
                profile.save()
                return HttpResponseRedirect(reverse('myforest', kwargs={"user_username": user_username}))
            else:
                Profiles.objects.filter(user_id=user).update(country=country, region=region, my_phrase=my_phrase, my_text=my_text)
                return HttpResponseRedirect(reverse('myforest', kwargs={"user_username": user_username}))
        else:
            return render(request, 'gotrees/edit_profile.html')

    else:
        return HttpResponseRedirect(reverse('index'))
