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
from Management.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view()),
    path('main/', MainHome.as_view(), name='mainHome'),
    path('courses/', courses.as_view(), name='courses'),
    path('courseEdit/', courseEdit.as_view()),
    path('sections/<int:course_id>/', sections.as_view(), name='sections'),
    path('sectionEdit/<int:course_id>/<int:section_id>/', sectionEdit.as_view(), name='sectionEdit'),
    path('sectionDelete/<int:course_id>/<int:section_id>/', sectionDelete.as_view(), name='sectionDelete'),
    path('sectionAdd/<int:course_id>/', sectionAdd.as_view(), name='sectionAdd'),
    path('accountEdit/', accountEdit.as_view(), name='accountEdit'),
    path('courseedit/<int:course_id>/', courseEdit.as_view(), name='courseedit'),
    path('notificationSend/', notificationSend.as_view(), name='notificationSend'),
    path('courseAdd/', courseAdd.as_view(), name='courseAdd'),
    path('courseDelete/<int:course_id>/', courseDelete.as_view(), name='courseDelete'),
    path('userToCourseAdd/<int:course_id>/', userToCourseAdd.as_view(), name='userToCourseAdd'),
    path('usersInCourse/<int:course_id>/', usersInCourse.as_view(), name='usersInCourse'),
    path('userAdd/', userAdd.as_view(), name='userAdd')

]
