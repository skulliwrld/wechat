from django.shortcuts import render,redirect
from chatapp.models import Room,Message
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="login")
def home(request):
    return render(request,'home.html')

def register(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():   
                messages.info(request,'email already exist')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'username already exist')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request,'passwords does not match')
            return redirect('register')
    return render(request,'register.html')

def login(request):
    if request.method == "POST":
        username= request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'credentials invalid')
            return redirect('login')
    else:
         return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def room(request,room):
    Username=request.GET.get('username')
    room_details=Room.objects.get(name=room)

    return render(request,'room.html',
    {"room_details":room_details,'username':Username,"room":room})

def checkview(request):
    room=request.POST['room_name']
    username=request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room +'/?username='+username)
    else:
        new_room=Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+ room +'/?username='+username)

def send(request):
    message=request.POST['message']
    username=request.POST['username']
    room_id =request.POST['room_id']

    new_messages= Message.objects.create(value=message ,user=username,room=room_id)
    new_messages.save()
    return HttpResponse('message sent successfully')

def getMessages(request,room):
    room_details=Room.objects.get(name=room)
    messages=Message.objects.filter(room=room_details.id)
    return JsonResponse({'messages':list(messages.values())})



