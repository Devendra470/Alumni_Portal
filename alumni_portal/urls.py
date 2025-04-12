"""
URL configuration for alumni_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
admin.site.site_header = "Gyan Ganga Alumni Admin"
admin.site.site_title = "Gyan Ganga Alumni Admin Portal"
admin.site.index_title = "Welcome to Gyan Ganga Alumni Portal"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('alumni.urls'))
]
