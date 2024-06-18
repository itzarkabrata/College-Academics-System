from django.shortcuts import render,HttpResponse
import random
from .models import Student,Marks,Department,Student_Id
from django.db.models import Q,Sum
from django.core.paginator import Paginator

# Create your views here.
def get_student(request):
    try:
        studentQuery = Student.objects.all()
    
        if(request.method == "POST"):
            query = request.POST.get("searchpara")
            studentQuery = Student.objects.filter(Q(stu_id__student_id__icontains = query)|Q(dept__department__icontains = query)|Q(stu_name__icontains = query)|Q(stu_email__icontains = query)|Q(stu_address__icontains = query))

        paginator = Paginator(studentQuery,6)  # Show 25 contacts per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        row_no = page_obj.start_index()

        return render(request,"report/table.html",context={"data":page_obj,"results" : len(studentQuery),"row_no":row_no})
    except Exception as e:
        print(e)

    return HttpResponse("No pages Found")


def get_marks(request,s_id):
    try:
        queryMarks = Marks.objects.filter(student_name__stu_id__student_id = s_id)
        queryStudent = Student.objects.filter(stu_id__student_id = s_id)
        if(len(queryMarks)!=0):
            student_name = queryMarks.first().student_name.stu_name
            total_marks = queryMarks.aggregate(total = Sum("marks"))
        else:
            queryMarks = False
            total_marks = {"total" : 0}
            student_name = queryStudent.first().stu_name
        return render(request,"report/marks.html",context={"data" : queryMarks,"total":total_marks,"student_name":student_name})
    except Exception as e:
        print(e)
    return HttpResponse("No Page Found")


def enlist_student(request):
    try:
        queryDept = Department.objects.all()

        department_list = []
        for i in range(len(queryDept)):
            department_list.append(queryDept[i].department) 

        if(request.method == "POST"):
            name = request.POST.get("name")
            email = request.POST.get("email")
            department_name = request.POST.get("department_name")
            address = request.POST.get("address")

            myid = department_name.upper()[0:3]+str(len(Student.objects.all())+1)+str(random.randint(10,100))

            new_sid = Student_Id.objects.create(student_id = myid)

            new_sdept = Department.objects.filter(department = department_name)[0]

            Student.objects.create(stu_id = new_sid,dept = new_sdept,stu_name = name,stu_email = email,stu_address = address)

        return render(request,"report/student.html",context={
            "department_list" : department_list
        })
    except Exception as e:
        print(e)

    return HttpResponse("Student Not added")


def enlist_dept(request):
    try:
        if(request.method=="POST"):
            deptname = request.POST.get("deptname")
            deptcode = int(request.POST.get("deptcode"))
            depthod = request.POST.get("depthod")

            Department.objects.create(department = deptname,code = deptcode,hod_name = depthod)

        queryDept = Department.objects.all()

        return render(request,"report/department.html",context={"data" : queryDept,"results" : len(queryDept)})
    except Exception as e:
        print(e)

    return HttpResponse("Deparment Not Added")

def delete_dept(request):
    pass