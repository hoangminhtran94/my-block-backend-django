from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict

from .models import Blog, Comment


def get_posts(request):
    blogs = Blog.objects.all().order_by(
        "-created_at")
    theList = list([])
    for blog in blogs:
        theList.append(blog.includeOwnerAndTags())

    return JsonResponse(theList, safe=False)


def get_post(request, postId):
    blog = Blog.objects.get(id=postId)

    return JsonResponse(blog.includeOwnerAndTags(), safe=False)


def add_comment(request, postId):
    if request.method == "POST":
        blog = Blog.objects.get(id=postId)
        print(request.body)
        return HttpResponse("success")
