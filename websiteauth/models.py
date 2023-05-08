from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.


class WebsiteUser(User):
    profile_picture = CloudinaryField("profile-picture")

    def getFullName(self):
        return f"{self.first_name} {self.last_name}"

    def getUserData(self):
        user_dict = {"firstname": self.first_name,
                     "fullname": f"{self.first_name} {self.last_name}",
                     "lastname": self.last_name,
                     "profilePicture": self.profile_picture.url,
                     "email": self.email}
        return user_dict
