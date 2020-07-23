from django.shortcuts import render,redirect
from .models import Schedule
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from webapp.models import User
from rest_framework.authtoken.models import Token
from .serializer import Sche_ser, UserSer, Sche_ser2
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie



# showing details through HTML page
def detail(request, slug):
    q = get_object_or_404(Schedule, slug=slug)
    cont ={'obj': q}
    return render(request, 'details.html', cont )

# managing event through HTML page
def dashboard(request):
    if not request.session.get('user'):
        return redirect('login')
    user = request.session.get('user')
    obj = User.objects.get(email=user)
    items = Schedule.objects.filter(reporter=obj).all()
    cont = {'items': items, 'user': obj}
    return render(request, 'dashboard.html', cont)

# creating new event through HTML page
def create(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        if request.method == "POST":
            title = request.POST.get('title')
            date = request.POST.get('date')
            event = request.POST.get('event')
            user = request.session.get('user')
            obj = User.objects.get(email=user)
            sched = Schedule()
            sched.title = title
            sched.event = event
            sched.date = date
            sched.reporter = obj
            sched.save()
            return redirect('dashboard')
        return render(request, 'create.html')


# editing event through HTML page
def edit(request, slug):
    if not request.session.get('user'):
        return redirect('login')
    else:
        user = request.session.get('user')
        obj = User.objects.get(email=user)
        usr = Schedule.objects.get(reporter=obj, slug=slug)
        cont = {'user': usr}
        if request.method == "POST":
            title = request.POST.get('title')
            date = request.POST.get('date')
            event = request.POST.get('event')
            user = request.session.get('user')
            obj = User.objects.get(email=user)
            usr.title = title
            usr.event = event
            usr.date = date
            usr.reporter = obj
            usr.save()
            return redirect('dashboard')
        return render(request, 'edit.html', cont)

# deleting event through HTML page
def delete(request, slug):
    if not request.session.get('user'):
        return redirect('login')
    else:
        user = request.session.get('user')
        obj = User.objects.get(email=user)
        usr = Schedule.objects.get(reporter=obj, slug=slug)
        cont = {'user': usr}
        usr.delete()
        return redirect('dashboard')

# -------------------------------------apiview---------------------------------


# getting event of authorized user through api

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def get_schedule(request, slug):
    token = request.headers['Authorization']
    token = token.replace("Token"," ",1)
    token = token.strip()
    user = Token.objects.get(key=token).user

    try:
        even = Schedule.objects.get(slug=slug)
        user2 = even.reporter
        if(user != user2):
           return Response({'response': "You don't have permission to view this"})
    except Schedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = Sche_ser(even)
    return Response(serializer.data)

# editing/modifying event of authorized user through api  (title,event,date are required)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def put_schedule(request, slug):
    try:
        token = request.headers['Authorization']
        token = token.replace("Token", " ", 1)
        token = token.strip()
        event = Schedule.objects.get(slug=slug)
        user1 = event.reporter
        user2 = Token.objects.get(key=token).user
        if (user1 != user2):
            return Response({'response': "You don't have permission to view this"})
    except Schedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = Sche_ser(event, data=request.data)
    if serializer.is_valid():
        val = serializer.save()
        event.title = val.title
        event.event = val.event
        event.date = val.date
        event.save()
        data = {}
        data['success'] = "Update successfully"
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# deleting event of authorized user through api
@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def del_schedule(request, slug):
    try:
        token = request.headers['Authorization']
        token = token.replace("Token", " ", 1)
        token = token.strip()
        even = Schedule.objects.get(slug=slug)
        user1 = even.reporter
        user2 = Token.objects.get(key=token).user
        if (user1 != user2):
            return Response({'response': "You don't have permission to view this"})
    except Schedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    operation = even.delete()
    data = {}
    if operation:
        data['success']= 'Delete Succesfull'
    else:
        data['fail'] ='failed'
    return Response(data=data)

# creating fresh new event of authorized user through api

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def post_schedule(request):
    token = request.headers['Authorization']
    token = token.replace("Token", " ", 1)
    token = token.strip()
    user = Token.objects.get(key=token).user
    even = Schedule(reporter=user)
    serializer = Sche_ser(even, data=request.data)
    if serializer.is_valid():
        data={}
        val = serializer.save()
        data['title'] = serializer.data['title']
        data['event'] = serializer.data['event']
        data['date'] = serializer.data['date']
        created = "Created Successfully for the user " + user.email
        data['success'] = created
        return Response(data=data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# getting all the events of a user through token

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def get_all_event(request):
    data = {}
    try:
        token = request.headers['Authorization']
        token = token.replace("Token", " ", 1)
        token = token.strip()
        user = Token.objects.get(key=token).user
        sche = Schedule.objects.filter(reporter=user).all()
    except User.DoesNotExist:
        data['failed'] = 'Invalid Token'
        return Response(data=data)
    if user:
        userSerializer = UserSer(user)
        serializer = Sche_ser2(sche, many=True)
        data['user'] = userSerializer.data['firstname'] + " " + userSerializer.data['lastname']
        data['events'] = serializer.data
        return Response(data=data)
    else:
        data['failed'] = 'Invalid login credentials'
        return Response(data=data)
