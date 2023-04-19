from django.contrib import admin
from .models import User, Course, Section, UsersToCourse


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "password", "phone", "role")


class CourseAdmin(admin.ModelAdmin):
    list_display = ("courseID", "courseName", "courseDescription", "courseDepartment")


class SectionAdmin(admin.ModelAdmin):
    list_display = ("sectionID", "location", "startTime", "endTime", "capacity", "TA", "courseID")


class UsersToCourseAdmin(admin.ModelAdmin):
    list_display = ("courseID", "assignment")


admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(UsersToCourse, UsersToCourseAdmin)
