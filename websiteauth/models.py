from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.


class WebsiteUser(User):
    profile_picture = CloudinaryField("profile-picture")
