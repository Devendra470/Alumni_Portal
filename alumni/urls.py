from django.contrib import admin
from django.urls import path ,include
from alumni import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage,name="homepage"),
    path('joinnetwork',views.signup,name="joinnetwork"),
    path('signin',views.signin,name='signin'),
    path("create_account",views.create_account,name="create_account"),
    path('signindata',views.signindata,name='signindata'),
    path('logout',views.logout,name='logout'),
    path('verify_otp',views.verify_otp,name="verify_otp"),
    path('resend_otp',views.resend_otp,name='resend_otp'),

    path('password_reset',views.password_reset,name='password_reset'),
    path('password_reset_page',views.password_reset_page,name='password_reset_page'),
    path('verify_password_otp',views.verify_password_otp,name='verify_password_otp'),
    path('new_password',views.new_password,name='new_password'),
    path('change_password',views.password_reset,name='change_password'),

    
    path('blog',views.blog,name='blog'),
    path('about_us',views.about_us,name='about_us'),
    path('alumni',views.alumni,name='alumni'),
    path('student',views.student,name='student'),
    path('myprofile',views.myprofile,name='myprofile'),
    path('profileupdate',views.profileupdate,name='profileupdate'),
    path('events',views.events,name='events'),
    path('propose_event',views.propose_event,name='propose_event'),
    path('internship',views.internship,name='internship'),
    path('jobs',views.jobs,name='jobs'),
    path('scholarships',views.scholarships,name='scholarships'),
    
]
if(settings.DEBUG):
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)