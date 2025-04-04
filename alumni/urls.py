from django.contrib import admin
from django.urls import path ,include
from alumni import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage,name="homepage"),
    path('joinnetwork',views.signup,name="signup"),
    path('signin',views.signin,name='signin'),
    path("create_account",views.create_account,name="create_account")
]