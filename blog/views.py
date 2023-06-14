
from django.http import HttpResponse, JsonResponse
import cloudinary
import cloudinary.uploader
from rest_framework.response import Response
from django.contrib.sessions.models import Session
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.utils.text import slugify

from websiteauth.models import WebsiteUser
from .models import Blog, Comment, Tag


def get_posts(request):
    blogs = Blog.objects.all().order_by(
        "-created_at")
    theList = list([])
    tags = Tag.objects.all().values()
    for blog in blogs:
        theList.append(blog.includeOwnerAndTags())

    print(theList)
    return JsonResponse({"blogs": theList, "tags": list(tags)}, safe=False)


def get_post(request, postId):
    id = int(postId)
    if (request.method == "GET"):
        blog = Blog.objects.get(id=id)
        return JsonResponse(blog.includeOwnerAndTags(), safe=False)
    if (request.method == "POST"):
        sessionId = request.COOKIES.get("sessionid")
        if not sessionId:
            return JsonResponse({'error': 'Session not found'}, status=404)

        session = Session.objects.get(session_key=sessionId)

        if not session:
            return JsonResponse({'error': 'Session not found'}, status=404)

        user_id = session.get_decoded().get('_auth_user_id')
        user = WebsiteUser.objects.get(user_ptr_id=user_id)
        if not user:
            return JsonResponse({'error': 'Unauthenticated'}, status=404)

        blog = Blog.objects.get(id=id)

        image = blog.image
        file = request.FILES.get("image")
        if (file):
            response = cloudinary.uploader.upload(
                file, folder="blog-media/blog-images")
            image = response["url"]

        data = request.POST
        blog.title = data.get("title")
        blog.content = data.get("content")
        blog.excerpt = data.get("excerpt")
        tags = data.getlist("tags")
        tagList = list([])
        for tag in tags:
            tagList.append(Tag.objects.get(caption=tag))
        blog.tags.set(tagList)
        blog.slug = slugify(data.get("title"))
        blog.image = image
        blog.save()
        if (file):
            return JsonResponse(blog.includeOwnerAndTagsOnCreated(), status=201)
        return JsonResponse(blog.includeOwnerAndTags(), status=201)


def add_a_blog(request):
    if (request.method == "POST"):
        sessionId = request.COOKIES.get("sessionid")
        if not sessionId:
            return JsonResponse({'error': 'Session not found'}, status=404)

        session = Session.objects.get(session_key=sessionId)

        if not session:
            return JsonResponse({'error': 'Session not found'}, status=404)

        user_id = session.get_decoded().get('_auth_user_id')
        user = WebsiteUser.objects.get(user_ptr_id=user_id)
        if not user:
            return JsonResponse({'error': 'Unauthenticated'}, status=404)

        file = request.FILES.get("image")
        response = cloudinary.uploader.upload(
            file, folder="blog-media/blog-images")

        data = request.POST
        title = data.get("title")
        content = data.get("content")
        excerpt = data.get("excerpt")
        image = response["url"]
        tags = data.getlist("tags")
        tagList = list([])
        for tag in tags:
            tagList.append(Tag.objects.get(caption=tag))
        slug = slugify(title)
        blog = Blog.objects.create(
            title=title, content=content, excerpt=excerpt, slug=slug, owner=user, image=image)
        blog.tags.set(tagList)
        blog.save()

        return JsonResponse(blog.includeOwnerAndTagsOnCreated(), status=201)
    return JsonResponse({'error': 'Not allowed'}, status=403)


def add_comment(request, postId):
    id = int(postId)
    if (request.method == "POST"):
        sessionId = request.COOKIES.get("sessionid")
        if not sessionId:
            return JsonResponse({'error': 'Session not found'}, status=404)

        session = Session.objects.get(session_key=sessionId)

        if not session:
            return JsonResponse({'error': 'Session not found'}, status=404)

        user_id = session.get_decoded().get('_auth_user_id')
        user = WebsiteUser.objects.get(user_ptr_id=user_id)
        if not user:
            return JsonResponse({'error': 'Unauthenticated'}, status=404)
        data = request.POST
        commentContent = data.get("comment")
        blog = Blog.objects.get(id=id)
        comment = Comment.objects.create(
            comment=commentContent, owner=user, post=blog)
        comment.save()
        return JsonResponse({"comment": commentContent, "owner": comment.getOwner()}, status=201)
