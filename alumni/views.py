from django.shortcuts import render
from django.http import HttpResponse
from .models import student

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
# Module to Signup Data 
def create_account(request):
    role=request.POST.get('role')
    firstname=request.POST.get('first_name')
    lastname=request.POST.get('last_name')
    email=request.POST.get('email')
    password=request.POST.get("password")
    gradyear=request.POST.get("grad_year",'')
    degree=request.POST.get('degree','')
    data=student.objects.all()
    if gradyear.isdigit():
        gradyear=int(gradyear)
    else:
        gradyear=None
    if degree=='':
        degree=None
    for saved_email in data:
        if(email==saved_email.email):
            return HttpResponse("Email Id already exists")
    student.objects.create(role=role,first_name=firstname,last_name=lastname,email=email,password=password,graduation_year=gradyear,degree=degree)
    return HttpResponse("Account Created Succesfully")

# Module for Signin Data
def signindata(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    params={'email':email,'password':password}
    return render(request,'alumni/signindata.html',params)