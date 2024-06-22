from django.shortcuts import render,redirect
import random
from .models import Student,Marks,Department,Student_Id,Subject
from django.db.models import Q,Sum
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.
@csrf_exempt
def home_screen(request):
    try:
        return render(request,"report/home.html")
    except Exception as e:
        print(e)
    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")


@csrf_exempt
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

    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")

@csrf_exempt
def get_marks(request,s_id):
    try:
        queryStudent = Student.objects.filter(stu_id__student_id = s_id)

        if(request.method == "POST"):
            subject_code = request.POST.get("subject_code")
            marks = request.POST.get("marks")

            sub_ins = Subject.objects.filter(sub_code = subject_code)

            Marks.objects.create(
                student_name = queryStudent[0],
                subject_name = sub_ins[0],
                marks = float(marks)
            )

            messages.success(request,"Marks added successfully")

        queryMarks = Marks.objects.filter(student_name__stu_id__student_id = s_id)

        if(len(queryMarks)!=0):
            student_name = queryMarks.first().student_name.stu_name
            total_marks = queryMarks.aggregate(total = Sum("marks"))
        else:
            queryMarks = False
            total_marks = {"total" : 0}
            student_name = queryStudent.first().stu_name

        student_dept = queryStudent.first().dept.department

        student_dept_code = queryStudent.first().dept.code

        sub_list = Subject.objects.filter(sub_dept__department = student_dept)

        return render(request,"report/marks.html",context={"data" : queryMarks,"total":total_marks,"student_info" :{"student_name":student_name,"student_dept" : student_dept,"student_dept_code":student_dept_code,"id" : s_id, "sub_list" : sub_list}})
    except Exception as e:
        print(e)
    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")

@csrf_exempt
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

            messages.success(request,"Student added successfully")

        return render(request,"report/student.html",context={
            "department_list" : department_list
        })
    except Exception as e:
        print(e)

    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")

@csrf_exempt
def enlist_dept(request):
    try:
        if(request.method=="POST"):
            deptname = request.POST.get("deptname")
            deptcode = int(request.POST.get("deptcode"))
            depthod = request.POST.get("depthod")

            Department.objects.create(department = deptname,code = deptcode,hod_name = depthod)

            messages.success(request,"Department Added Successfully")

        queryDept = Department.objects.all()

        return render(request,"report/department.html",context={"data" : queryDept,"results" : len(queryDept)})
    except Exception as e:
        print(e)

    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")


@csrf_exempt
def delete_dept(request,dept_code):
    try:
        if(request.method=="DELETE"):
            Department.objects.filter(code = dept_code).delete()

            messages.warning(request,f"Department with code {dept_code} deleted successfully")

        return redirect("enlistNewDepartment")
    except Exception as e:
        print(e)

    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")


@csrf_exempt
def delete_student(request,studentId):
    try:
        if(request.method=="DELETE"):
            Student_Id.objects.filter(student_id = studentId).delete()

            messages.warning(request,f"Student with id {studentId} deleted successfully")

        return redirect("/student-details/")
    except Exception as e:
        print(e)

    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")


@csrf_exempt
def show_dept_subjects(request,dept_name):
    try:
        if(request.method == "POST"):
            subject_name = request.POST.get("subname")

            dept_ins = Department.objects.filter(department = dept_name)[0]

            code = subject_name.upper()[0:3]+"-"+dept_name.upper()[0:2]+str(len(Subject.objects.all())+1)+str(random.randint(10,99))

            Subject.objects.create(
                sub_dept = dept_ins,
                sub_name = subject_name,
                sub_code = code
            )

            messages.success(request,f"Subject added successfully for Department of {dept_name}")

        subjects = Subject.objects.filter(sub_dept__department = dept_name)

        hod = subjects[0].sub_dept.hod_name

        code = subjects[0].sub_dept.code

        return render(request,"report/subjects.html",context={"dept_info":{"name" : dept_name,"hod" : hod,"code" : code},"subjects" : subjects})
    except Exception as e:
        print(e)

    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")


@csrf_exempt
def delete_dept_subject(request,subject_code):
    try:
        if(request.method=="DELETE"):
            sub_ins = Subject.objects.filter(sub_code = subject_code)
            subj_name = sub_ins[0].sub_name
            sub_ins.delete()

            messages.warning(request,"Department deleted succesfully")

        return redirect(f"/department/enlist/{subj_name}")
    except Exception as e:
        print(e)
    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")


@csrf_exempt
def delete_marks(request,student_identity):
    try:
        if(request.method == "GET"):

            s_code = request.GET.get("scode")

            Marks.objects.filter(student_name__stu_id__student_id = student_identity,subject_name__sub_code = s_code)[0].delete()
            messages.warning(request,"Marks Deleted Succesfully")

            return redirect(f"/marks/{student_identity}")
        
    except Exception as e:
        print(e)
    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")

@csrf_exempt
def profile_info(request,profile_code):
    try:
        stu_ins = Student.objects.filter(stu_id__student_id = profile_code)[0]

        return render(request,"report/profile.html",context={"stu_info" : stu_ins})
        
    except Exception as e:
        print(e)

    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")


@csrf_exempt
def login_page(request):
    try:
        if(request.method == "POST"):
            username = request.POST.get("username")
            password = request.POST.get("password")

            if(User.objects.filter(username = username).exists()):
                user = authenticate(username = username,password = password)

                if user is None:
                    messages.warning(request,"Invalid Password : Check your password again")
                    return redirect("/login/")
                
                else:
                    login(request,user)
                    messages.success(request,"Succesfully logged in")
                    return redirect("/student-details/")
            
            else:
                messages.warning(request,"Invalid Username : user not exits")
                return redirect("/login/")

        return render(request,"report/login.html")
        
    except Exception as e:
        print(e)

    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")

@csrf_exempt
def signup_page(request):
    try:
        if(request.method == "POST"):
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if(User.objects.filter(username = username).exists()):
                messages.warning(request,"Username already exists, Please try with other name")
                return redirect("/signup/")
            
            user = User.objects.create(
                username = username,
                email = email
            )

            user.set_password(password)
            user.save()
            
            messages.success(request,"Account created successfully")

        return render(request,"report/signup.html")
        
    except Exception as e:
        print(e)

    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")

def logout_page(request):
    try:
        logout(request)
        return redirect("/login/")

    except Exception as e:
        print(e)

    messages.warning(request,"Something went wrong at the server")
    return render(request,"report/error.html")