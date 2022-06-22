from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def register(request):

    


    return render(request, 'register.html')


def login_view(request):

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')

def forget(request):
    return render(request, 'forget.html')

def terms(request):
    return render(request, 'tac.html')

def logout_view(request):
    logout(request)
    return redirect('home')
    