"""
URL configuration for report_card project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from studentcard.views import get_student,get_marks,enlist_student,enlist_dept

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',get_student,name="student Info"),
    path('marks/<s_id>/',get_marks,name="studentID"),
    path('student/enlist/',enlist_student,name="enlistNewStudent"),
    path('department/enlist/',enlist_dept,name="enlistNewDepartment"),
]
