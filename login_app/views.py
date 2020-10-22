from django.shortcuts import render, redirect
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt
from time import gmtime, strftime

# Create your views here.

### LOGIN/REG PAGE RENDERING ###
def index(request):
    print('*'*100)
    print('This is the index route...')
    return render(request, 'index.html')

### REGISTRATION ###
def register(request):
    print('*'*100)
    print('Registering...')
    errors = User.objects.register_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        # hash password
        hashBrowns = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hashBrowns)
        
        # create a user
        user_just_registered = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashBrowns,
        )
        
        print("hashbrown password is:", hashBrowns)
        
        # create session
        request.session['uid'] = user_just_registered.id
        request.session['first_name'] = user_just_registered.first_name
        
        return redirect('/profile')

### LOGIN ###
def login(request):
    print('*'*100)
    print('Logging in...')
    errors = User.objects.log_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email']).first()
        request.session['uid'] = user.id
        request.session['first_name'] = user.first_name
        return redirect('/profile')
    
        #     if user != None:
        #     if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        #         request.session['uid'] = user.id
        #         request.session['first_name'] = user.first_name
        #     return redirect('/profile')
        # else:
        #     return redirect('/')
    
### PROFILE PAGE RENDERING ###
def profile(request):
    print('*'*100)
    print('on the profile page...')
    # check to if user is in session
    if "uid" not in request.session:
        return redirect("/")
    
    context = {
        "messages": Message.objects.all(),
        "comments": Comment.objects.all(),
    }
    return render(request, 'profile.html', context)

### ADDING MESSAGE ON WALL ###
def post_message(request):
    print('*'*100)
    print('creating message...')
    print(request.POST)
    
    logged_in_user = User.objects.get(id=request.session['uid'])
    
    # create message
    newMessage = Message.objects.create(
        message = request.POST["post_message"],
        user = logged_in_user
    )
    return redirect('/profile')

### COMMENTING ON A MESSAGE ###
def post_comment(request, message_id):
    print('*'*100)
    print('creating comment...')
    print(request.POST)
    
    logged_in_user = User.objects.get(id=request.session['uid'])
    
    # create message
    newComment = Comment.objects.create(
        comment = request.POST["post_comment"],
        user = logged_in_user,
        message = Message.objects.get(id= message_id)
    )
    return redirect('/profile')

### LOGOUT ###
def logout(request):
    print('*'*100)
    print('Clearing session and returning to login...')
    request.session.clear()
    return redirect('/')