import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import WebsiteUser
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
import cloudinary
import cloudinary.uploader
# Create your views here.


@api_view(["POST"])
def register(request):

    data = request.POST
    email = data.get("email")
    password = data.get("password")
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    file = request.FILES.get("profilePicture")
    response = cloudinary.uploader.upload(
        file, folder="blog-media/profile-pictures")

    user = WebsiteUser.objects.create_user(
        username=email, email=email, password=password)
    user.profile_picture = response["url"]
    user.first_name = firstname
    user.last_name = lastname

    user.save()
    return JsonResponse({"success": "User has been registerd"})


def loginUser(request):
    data = data = request.POST
    username = data.get("email")
    password = data.get("password")

    if username is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter username"
            }
        }, status=400)
    elif password is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter password"
            }
        }, status=400)
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        userdata = WebsiteUser.objects.get(username=user)
        session_key = request.session.session_key
        response = JsonResponse(
            {"success": "User has been logged in", "data": userdata.getUserData(), "sessionid": session_key})
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    return JsonResponse(
        {"errors": "Invalid credentials"},
        status=400,
    )


def logoutUser(request):
    try:
        logout(request)
    except:
        return JsonResponse(
            {"errors": "Error"})
    return JsonResponse({"message": "Success"}, status="201")
