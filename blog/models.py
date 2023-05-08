from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxLengthValidator
# Create your models here.
from websiteauth.models import WebsiteUser
from cloudinary.models import CloudinaryField


class Tag(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return self.caption


class Blog(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255, validators=[
                             MinLengthValidator(1)])
    content = models.TextField()
    excerpt = models.TextField()
    image = CloudinaryField("blog-images", null=True)
    owner = models.ForeignKey(
        WebsiteUser, on_delete=models.SET_NULL, related_name="posts", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    def includeOwnerAndTags(self):
        owner_dict = self.owner.getUserData()

        blog_dict = {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "content": self.content,
            "excerpt": self.excerpt,
            "image": self.image.url,
            "owner": owner_dict,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "tags": [tag.caption for tag in self.tags.all()],
            "comments": [{"comment": comment.comment, "owner": comment.getOwner()} for comment in self.comments.all()]
        }
        return blog_dict

    def includeOwnerAndTagsOnCreated(self):
        owner_dict = self.owner.getUserData()

        blog_dict = {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "content": self.content,
            "excerpt": self.excerpt,
            "image": self.image,
            "owner": owner_dict,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "tags": [tag.caption for tag in self.tags.all()]
        }
        return blog_dict


class Comment(models.Model):
    owner = models.ForeignKey(
        WebsiteUser, on_delete=models.SET_NULL, related_name="comments", null=True)
    comment = models.TextField()
    post = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="comments")

    def getOwner(self):
        user_dict = {"firstname": self.owner.first_name,
                     "fullname": f"{ self.owner.first_name} { self.owner.last_name}",
                     "lastname":  self.owner.last_name,
                     "profilePicture":  self.owner.profile_picture.url,
                     "email":  self.owner.email}
        return user_dict
