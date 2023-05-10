from django.shortcuts import render, redirect
from .models import ChatRoom,ChatMessage
from .forms import roomForm, LoginForm, UserRegister
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# Create your views here.

def loginRequired(request):
    if not request.user.is_authenticated:
        return render(request, "chatapp/login_error.html")

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username = data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return render(request,'chatapp/index.html')
            else:
                return HttpResponse('Invalid credentials')
    else:
        form = LoginForm()
        return render(request,'chatapp/login.html',{'form': form})
    
def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'chatapp/register_done.html')
    else:
        form = UserRegister()
    return render(request, 'chatapp/register.html', {'form': form})

def index(request):
    chatrooms = ChatRoom.objects.all()
    if request.user.is_authenticated:
        return render(request,'chatapp/index.html',{'chatrooms':chatrooms})
    else:
        return render(request,'chatapp/login_error.html')

def chatroom(request,slug):
    chatroom = ChatRoom.objects.get(slug=slug)
    messages = ChatMessage.objects.filter(room=chatroom)[0:30]
    return render(request,'chatapp/room.html',{'chatroom':chatroom,'messages':messages})

def addRoom(request):
    if request.user.is_authenticated:
        form = roomForm()
        if request.method == 'POST':
            form = roomForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
        return render(request, 'chatapp/addRoom.html', {'form': form})
    else:
        return render(request,'chatapp/login_error.html')

    

def about(request):
    return render(request, 'chatapp/about.html')
