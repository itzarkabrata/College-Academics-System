from django.db import models

# Create your models here.
class Department(models.Model):
    department = models.CharField(max_length=50,default=None,unique=True)
    code = models.IntegerField(default=None,unique=True)
    hod_name = models.CharField(max_length=100,default=None)

    class Meta:
        ordering = ['department']

    def __str__(self):
        return self.department
    
class Student_Id(models.Model):
    student_id = models.CharField(max_length=20,default=0)

    def __str__(self):
        return self.student_id
        
class Student(models.Model):
    stu_id = models.OneToOneField(Student_Id,related_name="studentId",on_delete=models.CASCADE)
    dept = models.ForeignKey(Department,related_name="dept",on_delete=models.CASCADE)
    stu_name = models.CharField(max_length=100,default="student")
    stu_email = models.EmailField(default=None,unique=True)
    stu_address = models.CharField(max_length=100,default=None)

    def __str__(self):
        return self.stu_name
    
    class Meta:
        ordering = ["stu_name"]
    

class Subject(models.Model):
    sub_name = models.CharField(max_length=70,default=None)
    sub_code = models.CharField(max_length=10,default=None,unique=True)

    def __str__(self):
        return self.sub_name
    
    class Meta:
        ordering = ["sub_name"]

class Marks(models.Model):
    student_name = models.ForeignKey(Student,related_name="StudentName",on_delete=models.CASCADE)
    subject_name = models.ForeignKey(Subject,related_name="subjectName",on_delete=models.CASCADE)
    marks = models.FloatField(default=0)

    def __str__(self):
        return (self.student_name.stu_name + " " + self.subject_name.sub_name)
    
    class Meta:
        ordering = ["student_name"]
    