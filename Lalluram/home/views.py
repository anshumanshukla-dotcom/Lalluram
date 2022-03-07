from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
# Create your views here.
def index(request):
    # return HttpResponse("this is homepage")
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        contact = Contact(name = name, email = email, desc = desc, date = datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request, 'contact.html')


def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            messages.success(request, "You've been successfully logged in!")
            return redirect("/")
        else:
            # No backend authenticated the credentials
            # VVI
            # messages.error(request, "Invalid Credentials! Try again.")
            return render(request, 'login.html')

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    # VVI
    # messages.success(request, "You've been successfully logged out!")
    return redirect("/login")


def handleSignup(request):
    if request.method == 'POST':
        # Get the post paramaters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous inputs
        # username should be under 10 characters
        if len(username) > 10:
            # VVI
            # messages.error(request, "Username must be less than 10 characters.")
            return redirect('home')
        # username should be alphanumeric
        if not username.isalnum():
            # VVI
            # messages.error(request, "Username should only contains letters and numbers.")
            return redirect('home')
        # passwords should match
        if pass1 != pass2:
            # VVI
            # messages.error(request, "Password and Confirm Password do not match.")
            return redirect('home')

        # create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account at Lalluram was created successfully.")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')


def signup2(request):
    return render(request, 'signup.html')


def search(request):
    query = request.GET['query']
    if len(query)>32:
        messages.error(request, "Your query was ignored because we limit queries to 32 words..")
    params = {'query':query}
    return render(request, 'search.html', params)
    # return HttpResponse('This is search.')