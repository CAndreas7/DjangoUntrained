"""DjangoUntrained URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from django.contrib import admin
from django.urls import path
from Management.views import Home, MainHome, courseEdit, editUserInCourse, EditSections, accountEdit, courses
#from ProjectApp.views import Home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view()),
    path('main/', MainHome.as_view()),
    path('courses/', courses.as_view(), name='courses'),
    path('courseEdit/', courseEdit.as_view()),
    path('sectionEdit', EditSections.as_view()),
    path('accountEdit/', accountEdit.as_view(), name='accountEdit'),
    path('courseedit/<int:course_id>/', courseEdit.as_view(), name='courseedit'),
]
