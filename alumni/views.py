from django.shortcuts import render
from django.http import HttpResponse

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
# Module to Create an Account 
def create_account(request):
    role=request.POST.get('role')
    firstname=request.POST.get('first_name')
    lastname=request.POST.get('last_name')
    email=request.POST.get('email')
    password=request.POST.get("password")
    gradyear=request.POST.get("grad_year",'default')
    degree=request.POST.get('degree','default')
    params={'role':role,'firstname':firstname,'lastname':lastname,'email':email,'password':password,'gradyear':gradyear,'degree':degree}
    return render(request,'alumni/data.html',params)