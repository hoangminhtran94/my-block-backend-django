from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxLengthValidator
# Create your models here.


class Tag(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return self.caption


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def getFullData(self):
        return {"first_name": self.first_name, "last_name": self.last_name, "email_address": self.email_address}

    def __str__(self):
        return self.full_name()


class Blog(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255, validators=[
                             MinLengthValidator(1)])
    content = models.TextField()
    excerpt = models.TextField()
    image = models.ImageField(upload_to="blog-images", null=True)
    owner = models.ForeignKey(
        Author, on_delete=models.SET_NULL, related_name="posts", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    def includeOwnerAndTags(self):
        owner_dict = {
            "full_name": self.owner.full_name(),
            "email_address": self.owner.email_address
        }
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
            "tags": [tag.caption for tag in self.tags.all()]
        }
        return blog_dict


class Comment(models.Model):
    owner = models.ForeignKey(
        Author, on_delete=models.SET_NULL, related_name="comments", null=True)
    comment = models.TextField()
    post = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="comments")
