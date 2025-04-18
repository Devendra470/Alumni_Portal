from django.contrib import admin
from django.urls import path ,include
from alumni import views
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
    path('password_reset',views.password_reset_page,name='password_reset'),
    path('change_password',views.passoword_reset,name='change_password'),
    path('blog',views.blog,name='blog'),
    
]