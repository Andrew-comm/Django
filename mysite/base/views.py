from multiprocessing import context
from re import I
from django.shortcuts import render
from .models import Room
from .forms import RoomForm
# Create your views here.
#rooms = [

#    {"id":1, "name":"Django startup"},
#   {"id":2, "name":"The Backend_Development"},
#    {"id":3, "name":"Absolute frontend"},
#]



def home(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render( request, 'home.html', context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, 'room.html',context)

def createRoom(request):
    form = RoomForm()
    context = {"form":form}
    
    return render (request,"room_form.html",context )

 