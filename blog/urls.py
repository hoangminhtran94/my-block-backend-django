from django.urls import path
from . import views


urlpatterns = [
    path("", views.get_posts),
    path("add-new/", views.addABlog),
    path("<postId>/", views.get_post),
    path("<postId>/comment/", views.add_comment),
    # path("<postId>", views.updateAPost),


]
