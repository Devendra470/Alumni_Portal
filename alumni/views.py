from django.shortcuts import render
from django.http import HttpResponse
from .models import Student,Alumni
from django.contrib.auth.hashers import make_password,check_password
import random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


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
    email=request.POST.get('email').lower()
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
        
    user_data={
                'role':role,
                'firstname':firstname,
                'lastname':lastname,
                'email':email.lower(),
                'password':password,
                'gradyear':gradyear,
                'degree':degree,
                'hashed_password':hashed_password
            }
    otp=''.join([str(random.randint(0,9)) for _ in range(6)]) #Generating Otp
    request.session['otp']=otp
    
    # Checking for role to fetch database
    if(role=='Alumni'):
        if Alumni.objects.filter(email=email).exists(): #Checking if email already exist
            return render(request,'alumni/joinnetwork.html',{'flag':True})
        
        # If email id does not exist
        else:
            request.session['user_data']=user_data
            send_otp(email,request.session['otp'])
            return render(request,'alumni/otp_verification.html')
    
    
    
    elif(role=='Student'):
        if Student.objects.filter(email=email).exists(): #Checking if email already exist
            return  render(request,'alumni/joinnetwork.html',{'flag':True})
        else:
            request.session['user_data']=user_data
            send_otp(email,request.session['otp'])
            return render(request,'alumni/otp_verification.html')

# Module to Sign in
def signindata(request):
    # Taking input from user using html form
    email=request.POST.get('email').lower()
    password=request.POST.get('password')
    
    # Finding the email first in alumni table then in student table
    try:
        user=Alumni.objects.get(email=email)
    except Alumni.DoesNotExist:
        try:
            user=Student.objects.get(email=email)

        except Student.DoesNotExist:
            return render(request,'alumni/signin.html',{'flag':True}) #If not Found in both functon returns
    firstname=user.first_name
    # If function does not return then email is found now check for password
    if(check_password(password,user.password)):
        #To be changed
        request.session['user_id']=user.id
        request.session['email']=user.email
        return render(request,'alumni/dashboard.html',{'name':firstname})
    else:
        #To be changed
        return render(request,'alumni/signin.html',{'flag':True})
    
#Module to Logout
def logout(request):
    request.session.flush()
    return render(request,'alumni/index.html')

# Module to validate otp
def verify_otp(request):
    if request.method=='POST':
        entered_otp=request.POST.get('otp')
        generated_otp=request.session.get('otp')
        # If correct otp is entered
        print(type(entered_otp))
        print(type(generated_otp))
        if(entered_otp==generated_otp):
            # Collecting the data from session
            signup_data=request.session.get('user_data')
            Create_user(signup_data)
            return render(request,'alumni/signin.html',{'created':True,'flag':False})
        # IF Incorrect Otp is entered
        else:   
            return render(request,'alumni/otp_verification.html',{'Invalid_Otp':True})


      
# Module for Sending Email
def send_otp(user_email,otp):
    subject="Your OTP for College Alumni Portal"
    html_content=render_to_string("alumni/otp_template.html",{'otp':otp})
    from_email=settings.EMAIL_HOST_USER
    to=[user_email]
    email=EmailMessage(subject,html_content,from_email,to)
    email.content_subtype="html"
    email.send()
    
    
    
# Module to Create a new user  
def Create_user(signup_data):
    if(signup_data['role']=='Alumni'):
                Alumni.objects.create(role=signup_data['role'],
                                      first_name=signup_data['firstname'],
                                      last_name=signup_data['lastname'],
                                      email=signup_data['email'],
                                      password=signup_data['hashed_password'],
                                      graduation_year=signup_data['gradyear'],
                                      degree=signup_data['degree'])
    elif(signup_data['role']=='Student'):
                Student.objects.create(role=signup_data['role'],
                                      first_name=signup_data['firstname'],
                                      last_name=signup_data['lastname'],
                                      email=signup_data['email'],
                                      password=signup_data['hashed_password'],
                                      graduation_year=signup_data['gradyear'],
                                      degree=signup_data['degree'])
    