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
    path('change_password',views.change_password,name='change_password'),
    path('passwd',views.password_change_page,name='passwd'),
]