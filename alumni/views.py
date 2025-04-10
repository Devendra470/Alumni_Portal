from django.shortcuts import render
from django.http import HttpResponse
from .models import Student,Alumni
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.
# Displaying Homepage
def homepage(request):
    return render(request,'alumni/index.html')

# Displaying Signup Page
def signup(request):
    return render(request,'alumni/joinnetwork.html')

# Displaying SIgnin Page
def signin(request):
    return render(request,'alumni/signin.html')

# Module to Signup
def create_account(request):
    # Collecting Data from html form
    role=request.POST.get('role')
    firstname=request.POST.get('first_name')
    lastname=request.POST.get('last_name')
    email=request.POST.get('email')
    password=request.POST.get("password")
    gradyear=request.POST.get("grad_year",'')
    degree=request.POST.get('degree','')
    hashed_password=make_password(password)
    
    # Checking if grad_year and degree is empty
    if gradyear.isdigit():
        gradyear=int(gradyear)
    else:
        gradyear=None
    if degree=='':
        degree=None
        
    # Checking for role to fetch database
    msg=''' Account Created Succesfully
    <a href="signin">Login In</a>
    '''
    if(role=='Alumni'):
        if Alumni.objects.filter(email=email).exists():
            return HttpResponse("Email Id already exists")
        Alumni.objects.create(role=role,first_name=firstname,last_name=lastname,email=email,password=hashed_password,graduation_year=gradyear,degree=degree)
        #To be changed
        return HttpResponse(msg)
    
    elif(role=='Student'):
        if Student.objects.filter(email=email).exists():
            return HttpResponse("Email Id already exists")
        Student.objects.create(role=role,first_name=firstname,last_name=lastname,email=email,password=hashed_password,graduation_year=gradyear,degree=degree)
        #To be changed
        return HttpResponse(msg)

# Module to Sign in
def signindata(request):
    # Taking input from user using html form
    email=request.POST.get('email')
    password=request.POST.get('password')
    
    # Finding the email first in alumni table then in student table
    try:
        user=Alumni.objects.get(email=email)
    except Alumni.DoesNotExist:
        try:
            user=Student.objects.get(email=email)

        except Student.DoesNotExist:
            return HttpResponse("Invalid Email ID or Password") #If not Found in both functon returns
    firstname=user.first_name
    # If function does not return then email is found now check for password
    if(check_password(password,user.password)):
        #To be changed
        return render(request,'alumni/dashboard.html',{'name':firstname})
    else:
        #To be changed
        return HttpResponse("Invalid Email or Password") 
    