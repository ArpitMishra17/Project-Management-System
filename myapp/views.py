from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator
from .models import Employee,Project,Department,Designation,projectDepartment
# Create your views here.

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