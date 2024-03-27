from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import todo
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    if request.method == "POST":
        task = request.POST.get('task')
        new_task = todo(user = request.user, name = task)
        new_task.save()
    all_todos = todo.objects.filter(user = request.user)
    context = {
        'todos' : all_todos
    }
    return render(request, 'todo.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 8:
            messages.error(request, 'Password must be atleast 8 characters')
            return redirect('register')
        
        existing_username = User.objects.filter(username = username)
        if existing_username:
            messages.error(request, 'Username Already Exists ! \n Try Another One')
            return redirect('register')
        
        existing_email = User.objects.filter(email = email)
        if existing_email:
            messages.error(request, 'Email Already Exists ! \n Try Login')
            return redirect('register')

        user = User.objects.create_user(username=username, email = email, password = password)
        user.save()
        messages.success(request, 'Account Successfully Created!')
        return redirect('login')

    return render(request, 'register.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        validate_user = authenticate(username = username, password = password)
        if validate_user:
            login(request, validate_user)
            messages.success(request, 'Account Successfully Logged in!')
            return redirect('home')
        else:
            messages.error(request, 'User Does Not Exists!')
            return redirect('login')
        
    return render(request, 'login.html')

def delete(request, name):
    get_todo = todo.objects.get(user = request.user, name = name)
    get_todo.delete()
    return redirect('home') 

def update(request, name):
    get_todo =  todo.objects.get(user = request.user, name = name)
    get_todo.status = True
    get_todo.save()
    return redirect('home')

def logoutpage(request):
    logout(request)
    return redirect('login')