from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profiles(models.Model):
    image = models.CharField(max_length=30,blank=True)
    country = models.CharField(max_length=30, blank=True)
    region = models.CharField(max_length=30, blank=True)
    my_phrase = models.CharField(max_length=100, blank=True)
    my_text = models.CharField(max_length=400, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return f"{self.country} - {self.region} - {self.my_phrase} - {self.my_text}"

class Trees(models.Model):
    type = models.CharField(max_length=30)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trees")
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} - {self.user_id} - {self.time}"
