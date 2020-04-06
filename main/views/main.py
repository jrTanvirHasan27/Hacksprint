from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def index(request):
    if request.user.is_authenticated:
        return render(request, 'userpanel/index.html')
    else:
        return render(request, 'main/index.html')


def login_fn(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'GET':
            return render(request, 'main/login.html')

        elif request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'main/login.html', {'msg': 'Invalid username and password'})


def logout_fn(request):
    logout(request)
    return redirect('home')


def register_fn(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'GET':
            return render(request, 'main/register.html')

        elif request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email'] + '@diu.edu.bd'
            password = request.POST['password']

            username_count = User.objects.filter(username=username).count()
            email_count = User.objects.filter(email=email).count()

            if username_count == 0 and email_count == 0:
                User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_active=False)
                return redirect('login')

            elif username_count > 0:
                return render(request, 'main/register.html', {'msg': 'This username is in used'})

            elif email_count > 0:
                return render(request, 'main/register.html', {'msg': 'This email is in used'})
