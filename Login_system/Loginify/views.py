from django.http import HttpResponse, JsonResponse
from .serializer import UserDetailsSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from .models import UserDetails
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def home(request):
    return HttpResponse('<h1>Hello World</h1>')


# def login_page(request):
#     return render(request, 'Loginify/Login_page.html')

# def signup_page(request):
#     return render(request, 'Loginify/signup_page.html')


def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'Loginify/signup_page.html')

        if UserDetails.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'Loginify/signup_page.html')

        UserDetails.objects.create(username=username, email=email, password=password)
        messages.success(request, "Signup successful! Please login.")
        return redirect('login')  # match with your url name

    return render(request, 'Loginify/signup_page.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        try:
            user = UserDetails.objects.get(username=username)
            if user.password == password:
                return render(request, 'Loginify/success.html', {'user': user})
            else:
                messages.error(request, "Incorrect password.")
        except UserDetails.DoesNotExist:
            messages.error(request, "User not found.")

    return render(request, 'Loginify/Login_page.html')


@api_view(['GET'])
def get_all_users(request):
    users = UserDetails.objects.all()
    serializer = UserDetailsSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user_by_username(request, username):
    try:
        user = UserDetails.objects.get(username=username)
    except UserDetails.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
    serializer = UserDetailsSerializer(user)
    return Response(serializer.data)


@api_view(['PUT'])
def update_user(request, username):
    try:
        user = UserDetails.objects.get(username=username)
    except UserDetails.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
    serializer = UserDetailsSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_user(request, email):
    try:
        user = UserDetails.objects.get(email=email)
    except UserDetails.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
    user.delete()
    return Response({'message': 'User deleted successfully'}, status=204)