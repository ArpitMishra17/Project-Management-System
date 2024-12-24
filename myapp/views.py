from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from .models import Employee,Project,Department,Designation,projectDepartment
from django.http import JsonResponse
# Create your views here.

def employee_login(request):
    if request.method == 'POST':

        
        employee_email=request.POST.get('employee_email',None)
        employee_password=request.POST.get('employee_password',None)

        print("employee_email" , employee_email)
        print("employee_password" , employee_password)

        employee=authenticate(request,email=employee_email, password=employee_password)


        #print(employee.is_staff )

        if employee:

            if employee.designation and employee.designation.name in ["Project Manager","Senior Manager"]:
                login(request,employee)
                return redirect("manager_home")
            else:
                login(request,employee)
                return redirect("test_employee")
        else:
            
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    

    return render(request, 'login.html')

def adminpage(request):
    

    return render(request, 'adminpage.html')

def add_employee(request):
    if request.method=='POST':
        name=request.POST.get('employee_name', None)
        email=request.POST.get('employee_email',None)
        age=request.POST.get('employee_age',None)
        phone=request.POST.get('employee_phone',None)
        designation_id=request.POST.get('employee_designation',None)
        department_id=request.POST.get('employee_department',None)

        designation = Designation.objects.get(id=designation_id)
        department = Department.objects.get(id=department_id)

        employee=Employee.objects.create(
            name=name,
            email=email,
            age=age,
            phone=phone,
            designation=designation,
            department=department  
            )
        
        employee.save()

        return redirect('adminpage')
    
    context={
        'designation_choices':Designation.objects.all(),
        'department_choices':Department.objects.all()
    }

    return render(request, 'add_employee.html', context)


def add_project(request):
    if request.method=='POST':
        name=request.POST.get('project_name', None)
        date_of_receive=request.POST.get('project_date_of_receive',None)
        duration=request.POST.get('project_duration',None)
        project_department_id=request.POST.get('project_department',None)
        hours=request.POST.get('project_hours',None)
        
        project_department=projectDepartment.objects.get(id=project_department_id)

        project=Project.objects.create(
            name=name,
            date_of_receive=date_of_receive,
            duration=duration,
            project_department=project_department,
            hours=hours  
            )
        
        project.save()

        return redirect('adminpage')
    
    context={
        'department_choices':projectDepartment.objects.all()
    }

    return render(request, 'add_project.html', context)

def add_department(request):
    if request.method=='POST':
        name=request.POST.get('department_name', None)
       

        deparment=Department.objects.create(
            name=name
            )
        
        deparment.save()

        return redirect('adminpage')
    

    return render(request, 'add_department.html')

def add_designation(request):
    if request.method=='POST':
        name=request.POST.get('designation_name', None)
       

        designation=Designation.objects.create(
            name=name
            )
        
        designation.save()

        return redirect('adminpage')
    

    return render(request, 'add_designation.html')

def add_project_department(request):
    if request.method=='POST':
        name=request.POST.get('project_department_name', None)
       

        project_deparment=projectDepartment.objects.create(
            name=name
            )
        
        project_deparment.save()

        return redirect('adminpage')
    

    return render(request, 'add_project_department.html')

def display_employees(request):
    employee=Employee.objects.all()

    paginator=Paginator(employee,6)

    page_number= request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    return render(request, 'display_employees.html', {'page_obj':page_obj})

def display_projects(request):
    project=Project.objects.all()

    paginator=Paginator(project,6)

    page_number= request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    return render(request, 'display_projects.html', {'page_obj':page_obj})


def display_designations(request):
    designation=Designation.objects.all()

    paginator=Paginator(designation,6)

    page_number= request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    return render(request, 'display_designations.html', {'page_obj':page_obj})

def display_departments(request):
    department=Department.objects.all()

    paginator=Paginator(department,6)

    page_number= request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    return render(request, 'display_departments.html', {'page_obj':page_obj})

def display_project_departments(request):
    project_department=projectDepartment.objects.all()

    paginator=Paginator(project_department,6)

    page_number= request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    return render(request, 'display_project_departments.html', {'page_obj':page_obj})

def project_home(request,project_id):

    project=get_object_or_404(Project,id=project_id)

    employees=Employee.objects.filter(designation__name__in=["Senior Manager","Project Manager"])

    if request.method =="POST":
        manager_id=request.POST.get('manager_id')

        if manager_id:
            manager = get_object_or_404(Employee, id=manager_id)
            manager.projects.add(project)
            manager.save()
            return redirect('display_projects', project_id=project.id)
        
        

    context={
        'employees':employees,
        'project':project
    }

    return render(request,'project_home.html',context)

def test_employee(request):

    return render(request,'test_employee.html')

def manager_home(request):

    employee=Employee.objects.get(email=request.user.email)

    return render(request,'manager_home.html',{'employee':employee})




def manager_project_home(request,project_id):
    
    project=get_object_or_404(Project,id=project_id)
    designations = Designation.objects.all()

    if request.method == "POST":
        designation= request.POST.get('designation')
        employee_id= request.POST.get('employee') 

        if employee_id:
            employee=get_object_or_404(Employee,id=employee_id)
            project.employees.add(employee)
            return redirect('manager_project_home',project_id=project.id)
           
    

    context={
        'project':project,
        'designations':designations,
        'employees':Employee.objects.all(),
    }

    return render(request,'manager_project_home.html',context)

def get_employees_by_designation(request):
    designation=request.GET.get('designation')
    employees= Employee.objects.filter(designation=designation).values('id','name')
    return JsonResponse(list(employees),safe=False)