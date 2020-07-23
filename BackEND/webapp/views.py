from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSer, loginSer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_protect


# Create your views here.

# for registration of user through html page without api

def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User()
        user.firstname = firstname
        user.lastname = lastname
        user.email = email
        user.password = password

        try:
            user.save()
            return redirect('register')
        except:
            con = {'msg': " Email Already Exist!"}
            return render(request, 'register.html', con)

    return render(request, "register.html")


# for login of user through html page without api

def login_view(request):
    if not request.session.get('user'):
        if request.method == "POST":
            username = request.POST.get('email')
            password = request.POST.get('password')
            users = User.objects.filter(email=username, password=password)
            if users.exists():
                request.session['user'] = username
                return redirect('dashboard')
            else:
                return render(request, 'login.html')
        return render(request, 'login.html')
    else:
        return redirect('dashboard')

# for logout of user through html page without api

def logout(request):
    try:
        del request.session['user']
        return redirect('login')
    except:
        return HttpResponse("Session Timeout <a href='\webapp\login_view'>login again</a>")


# ---------------------------------all api views----------------------------


# for creating a fresh user through api

@api_view(['POST', ])
@permission_classes([AllowAny,])
def post_user(request):
    user = User()
    data = {}
    serializer = UserSer(user, data=request.data)
    if serializer.is_valid():
        val = serializer.save()
        data['firstname'] = val.firstname
        data['lastname'] = val.lastname
        data['email'] = val.email
        data['password'] = val.password
        data['success'] = 'Registered Successfully'
        data['token'] = Token.objects.get(user=val).key
        return Response(data=data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# for editing/modifying information of a logged in authorized user through api by token verification

@api_view(['PUT', ])
def put_user(request):
    try:
        user = User.objects.get(email=request.data['email'])
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    usr = request.user
    if user != usr:
        return Response({'response': "Invalid Login Credentials"})
    serializer = UserSer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {}
        data['success'] = "Update successfully"
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for getting token of user by login through api

@api_view(['POST', 'PUT', ])
@permission_classes([AllowAny,])
def post_login(request):
    data = {}
    try:
        email = request.data['email']
        password = request.data['password']
        users = User.objects.get(email=email, password=password)
    except User.DoesNotExist:
        data['failed'] = 'Invalid login credentials'
        return Response(data=data)
    if users:
        serializer = loginSer(users, data=request.data)
        if serializer.is_valid():
            ussr= serializer.save()
            token = Token.objects.get(user=ussr).key
            data['token'] = token
            data['userFirstname'] = ussr.firstname
            data['userLastname'] = ussr.lastname
            return Response(data=data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        data['failed'] = 'Invalid login credentials'
        return Response(data=data)
