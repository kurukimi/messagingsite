from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q

def home(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = rooms.count()

    if is_ajax:
        html = render_to_string(template_name="base/partial_room.html", context={'rooms' : rooms, 'room_count':room_count})
        dataDict = {'rooms' : html}
        return JsonResponse(dataDict, safe=False)

    topics = Topic.objects.all()
    context = {'rooms' : rooms, 'topics' : topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, 'base/room.html', context)


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    context = {'obj': room}
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)
