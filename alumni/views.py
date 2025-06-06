from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User,Events
from django.contrib.auth.hashers import make_password,check_password
import random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


# Displaying Homepage
def homepage(request):
    profile_pic = request.session.get('profile_pic')    
    params={'profile_pic':profile_pic}
    return render(request,'alumni/index.html',params)

# Displaying Signup Page
def signup(request):
    return render(request,'alumni/joinnetwork.html')

# Displaying Signin Page
def signin(request):
    return render(request,'alumni/signin.html')

# Module to display password change page
def password_reset(request):
    return render(request,'alumni/password_reset.html',{'step':1})

# Module to display About Us page
def about_us(request):
    profile_pic = request.session.get('profile_pic')    
    params={'profile_pic':profile_pic}
    return render(request,'alumni/aboutus.html',params)

# Module to display events page
def events(request):
    profile_pic = request.session.get('profile_pic')  
    events=Events.objects.filter(is_active=True).order_by("date").values("title","description","date","time","location")  
    params={'profile_pic':profile_pic,'events':events}
    return render(request,'alumni/events.html',params)

# Module for displaying Propose Event Page
def propose_event(request):
    profile_pic=request.session.get('profile_pic')
    return render(request,'alumni/propose_event.html',{'profile_pic':profile_pic})

# Module for Displaying Internship Page
def internship(request):
    return HttpResponse("This is Internship Page")

# Module for Diplaying Scholarship Page
def scholarships(request):
    return HttpResponse("This is Scholarship Page")

# Module for diplaying Job Page
def jobs(request):
    return HttpResponse("This is job Page")

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
                'gradyear':gradyear,
                'degree':degree,
                'hashed_password':hashed_password
            }
    
    #Generating Otp
    otp=''.join([str(random.randint(0,9)) for _ in range(6)]) 
    request.session['otp']=otp
    
    if (User.objects.filter(email=email).exists()): #Checking if email already exist
        return render(request,'alumni/joinnetwork.html',{'error':'Email ID already exist'})
        
    # If email id does not exist then send otp
    else:
        request.session['user_data']=user_data
        send_otp(email,request.session['otp'],role)
        return render(request,'alumni/otp_verification.html')

# Module to Sign in
def signindata(request):
    # Taking input from user using html form
    entered_email=request.POST.get('email').lower()
    password=request.POST.get('password')
    logged_user=None
    role=None
    # Finding the in User Table and taking the data into logged_user
    try:
        logged_user=User.objects.get(email=entered_email)
        role=logged_user.role
    except User.DoesNotExist:
        return render(request,'alumni/signin.html',{'error':'Invalid User ID or Password'}) #If not Found functon returns
    firstname=logged_user.first_name
    # If function does not return then email is found now check for password
    if(check_password(password,logged_user.password)):
        request.session['user_id']=logged_user.id
        request.session['email']=logged_user.email
        request.session['name']=logged_user.first_name
        request.session['role']=role 
        request.session['profile_pic']=logged_user.profile_pic.url if logged_user.profile_pic else None 
        if(role=='Alumni'):
            return render(request,'alumni/alumni.html',{'name':firstname})
        elif(role=='Student'):
            return render(request,'alumni/student.html',{'name':firstname})
    else:
        return render(request,'alumni/signin.html',{'error':'Invalid User Id or Password'})
 
    
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
            return render(request,'alumni/signin.html',{'created':True,'error':False})
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
    User.objects.create(role=signup_data['role'],
                        first_name=signup_data['firstname'],
                        last_name=signup_data['lastname'],
                        email=signup_data['email'],
                        password=signup_data['hashed_password'],
                        graduation_year=signup_data['gradyear'],
                        degree=signup_data['degree'])
# Module to Change Password
def password_reset_page(request):
    if request.method=='POST':
        email=request.POST.get('email')
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request,'alumni/password_reset.html',{'step':1,'error':'Invalid Email Id.'})
        otp=''.join([str(random.randint(0,9)) for _ in range(6)]) 
        request.session['password_reset_otp']=otp
        request.session['password_reset_email']=email
        send_otp(email,otp,None)
        return render(request,'alumni/password_reset.html',{'step':2})
    return render (request,'alumni/password_reset.html',{'step':1})

def verify_password_otp(request):
    entered_otp=request.POST.get('otp')
    if(entered_otp==request.session.get('password_reset_otp')):
        return render(request,'alumni/password_reset.html',{'step':3})
    else:
        return render(request,'alumni/password_reset.html',{'step':2,'error':'Invalid OTP'})

def new_password(request):
    new_password=request.POST.get('new_password')
    confirm_password=request.POST.get('confirm_password')
    if(new_password==confirm_password):
        email=request.session.get('password_reset_email')
        if not email:
            return redirect('password_reset')
        user=User.objects.get(email=email)
        user.password=make_password(new_password)
        user.save()
        request.session.pop('password_reset_otp')
        request.session.pop('password_reset_email')
        return render(request,'alumni/password_reset.html',{'step':4})
    else:
        return render(request,'alumni/password_reset.html',{'step':3,'error':"Password Does not Match"})


        




# Module to display blog page
def blog(request):
    if(request.session.get('user_id')==None):
        return redirect(signin)
    else:
        return render(request,'alumni/blog1.html')



# Module to display alumni page from homepage
def alumni(request):
    if(request.session.get('user_id')==None):
        return redirect(signin)
    else:
        role=request.session.get('role')
        
        if(role=='Alumni'):
            return render(request,'alumni/alumni.html')
        else:
            return render(request,'alumni/student.html')
  
  
    
# Module to display student page from homepage   
def student(request):
    if(request.session.get('user_id')==None):
        return redirect('signin')
    else:
        role=request.session.get('role')
        if(role=='Student'):
            return render(request,'alumni/student.html')
        else:
            return render(request,'alumni/alumni.html')
        
# Module for My Profile data
def myprofile(request):
    user_email_id=request.session.get('email')
    if(user_email_id==None):
        return redirect(signin)
    user=User.objects.get(email=user_email_id)
    params={'grad_year':user.graduation_year,
            'role':user.role,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email_id':user_email_id,
            'linkedin_url':'',
            'github_url':'',
            'bio':'',
            'profile_url':user.profile_pic.url if user.profile_pic else None,
            'username':user.username
            }
    return render(request,'alumni/studentprofile.html',params)

# Module for updating profile
def profileupdate(request):
    if (request.method=='POST'):
        profile_pic=request.FILES.get('profile_pic')
        user_id=request.session.get('user_id')
        if not user_id:
            return redirect(signin)
        user=User.objects.get(id=user_id)
        if profile_pic:
            user.profile_pic=profile_pic
        user.username=request.POST.get('username')   
        user.grad_year=request.POST.get('grad_year')
        user.firstname=request.POST.get('first_name')
        user.lastname=request.POST.get('last_name')
        user.role=request.POST.get('role')
        user.linkedinurl=request.POST.get('linkedin_url')
        user.githuburl=request.POST.get('github_url')
        user.bio=request.POST.get('bio')
        user.save()
        request.session['profile_pic']=user.profile_pic.url if user.profile_pic.url else None
        return redirect('myprofile')
    else:
        return HttpResponse("404 Not Allowed")