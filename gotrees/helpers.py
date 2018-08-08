from django.contrib.auth.models import User
from .models import Profiles
import os

def upload_file(file, user_username):
    """Upload image to profiles"""
    if file.size < 2500000:
        list = ["jpg", "jpeg", "png"]
        end = (file.name).split(".")[1].lower()

        if end in list:
            user = User.objects.get(username=user_username)
            profile = Profiles.objects.get(user_id=user)
            if profile.image != '':
                os.remove('gotrees/static/gotrees/uploads/' + profile.image)
            name = (file.name).split(".")[0] + "." + end
            with open('gotrees/static/gotrees/uploads/' + name, 'wb+') as destination:
                for chunk in file.chunks():
                    print('Something')
                    destination.write(chunk)
            profile.image = name
            profile.save()
            return name
        else:
            return False
    else:
        return False

def get_profile(user_username):
    """Serve context for profile and edit_profile"""
    user = User.objects.get(username=user_username)

    context = {
    "user_username": user_username,
    "first_name": user.first_name,
    "country": user.profile.all()[0].country,
    "region": user.profile.all()[0].region,
    "my_phrase": user.profile.all()[0].my_phrase,
    "my_text": user.profile.all()[0].my_text,
    "image": user.profile.all()[0].image
    }
    return context

if __name__ == "__main__":
    main()
