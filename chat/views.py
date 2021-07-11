from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room
from register.models import event_contrib

@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    room=[]
    check= event_contrib.objects.filter(user=request.user)
    for x in check:
        room.append(x.event_id.event_name)

    print(room)


    print(request.user,type(request.user),request.user.username,type(request.user.username))
    rooms = []
    for r in room:
        if(Room.objects.filter(title=r)):
            rooms.append(Room.objects.filter(title=r))
    #rooms = Room.objects.order_by("title")
    print(rooms,type(rooms))
    # Render that in the index template
    return render(request, "chat/index.html", {
        "rooms": rooms,
    })
