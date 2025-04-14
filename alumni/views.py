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
    degree=degree or None
             
    # Storing User Data into Template to create session 
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
    
    #Generating Otp
    otp=''.join([str(random.randint(0,9)) for _ in range(6)]) 
    request.session['otp']=otp
    
    # Checking for role to fetch database
    if(role=='Alumni'):
        if (Alumni.objects.filter(email=email).exists()) or (Student.objects.filter(email=email).exists()): #Checking if email already exist
            return render(request,'alumni/joinnetwork.html',{'flag':True})
        
        # If email id does not exist then send otp
        else:
            request.session['user_data']=user_data
            send_otp(email,request.session['otp'],role)
            return render(request,'alumni/otp_verification.html')
    
    elif(role=='Student'):
        if (Student.objects.filter(email=email).exists() )or (Alumni.objects.filter(email=email).exists()) : #Checking if email already exist
            return  render(request,'alumni/joinnetwork.html',{'flag':True})
        
        else:
            request.session['user_data']=user_data
            send_otp(email,request.session['otp'],role)
            return render(request,'alumni/otp_verification.html')

# Module to Sign in
def signindata(request):
    # Taking input from user using html form
    email=request.POST.get('email').lower()
    password=request.POST.get('password')
    user=None
    role=None
    # Finding the email first in alumni table then in student table
    try:
        user=Alumni.objects.get(email=email)
        role='Alumni'
    except Alumni.DoesNotExist:
        try:
            user=Student.objects.get(email=email)
            role='Student'
        except Student.DoesNotExist:
            return render(request,'alumni/signin.html',{'flag':True}) #If not Found in both functon returns
    firstname=user.first_name
    # If function does not return then email is found now check for password
    if(check_password(password,user.password)):
        request.session['user_id']=user.id
        request.session['email']=user.email
        request.session['name']=user.first_name
        request.session['role']=role  
        if(role=='Alumni'):
            return render(request,'alumni/alumni.html',{'name':firstname})
        elif(role=='Student'):
            return render(request,'alumni/student.html',{'name':firstname})
    else:
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
        if(entered_otp==generated_otp):
            # Collecting the data from session
            signup_data=request.session.get('user_data')
            Create_user(signup_data)
            request.session.pop('otp',None)
            return render(request,'alumni/signin.html',{'created':True,'flag':False})
        # IF Incorrect Otp is entered
        else:   
            return render(request,'alumni/otp_verification.html',{'Invalid_Otp':True})


# Module for Sending Email
def send_otp(user_email,otp,role):
    subject="Your OTP for College Alumni Portal"
    html_content=render_to_string("alumni/otp_template.html",{'otp':otp,'role':role})
    from_email=settings.EMAIL_HOST_USER
    to=[user_email]
    email=EmailMessage(subject,html_content,from_email,to)
    email.content_subtype="html"
    email.send()

# Module to resend otp
def resend_otp(request):
    signup_data=request.session.get('user_data')   
    user_email=signup_data['email']
    otp=''.join([str(random.randint(0,9)) for _ in range(6)]) 
    request.session['otp']=otp
    role=signup_data['role']
    send_otp(user_email,otp,role)
    return render(request,'alumni/otp_verification.html',{'resend_otp':True})
    
    
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
    