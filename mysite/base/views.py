from multiprocessing import context
from re import I
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib .auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from zmq import Message

from .models import Room, Topic, Message
from .forms import RoomForm
# Create your views here.
#rooms = [

#    {"id":1, "name":"Django startup"},
#   {"id":2, "name":"The Backend_Development"},
#    {"id":3, "name":"Absolute frontend"},
#]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')

        else:
            messages.error(request, "username OR password does not exist")



    context = {'page':page}
    return render(request,"login.html",context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
            

        else:
            messages.error(request, "An error occured during registration")



    context ={'form':form}
    return render(request,"login.html", context)




def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count}
    return render( request, 'home.html', context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    
    if request.method == 'POST':
        message = Message.objects.create(

            user=request.user,
            room=room,
            body=request.POST.get("body")

        )
        return redirect('room', pk=room.id)




    context = {'room':room, 'room_messages':room_messages}
    return render(request, 'room.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    context = {"form":form}
    
    if request.method == 'POST':
         form = RoomForm(request.POST)
         if form.is_valid():
            form.save()
            return redirect('home')

        
    
    return render (request,"room_form.html",context )

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("you are not allowed here!!")

    if request.method == 'POST':
        form = RoomForm(request.POST)
        form.is_valid()
        form.save()
        return redirect('home')
    
    context = {'form':form}
    
    
    return render(request, "room_form.html",context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)


    if request.user != room.host:
        return HttpResponse("you are not allowed here!!")
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
        
    return render(request, "delete.html",{'obj':room})

        
      


 