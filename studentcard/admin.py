from django.contrib import admin
from .models import Student,Department,Student_Id,Marks,Subject

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["stu_id","dept","stu_name","stu_email","stu_address"]

admin.site.register(Student_Id)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["department","code","hod_name"]

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ["student_name","subject_name","marks"]

@admin.register(Subject)
class SubjcetAdmin(admin.ModelAdmin):
    list_display = ["sub_dept","sub_name","sub_code"]