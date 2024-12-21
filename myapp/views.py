from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator
from .models import Employee,Project
# Create your views here.

def adminpage(request):
    

    return render(request, 'adminpage.html')

def add_employee(request):
    if request.method=='POST':
        name=request.POST.get('employee_name', None)
        email=request.POST.get('employee_email',None)
        age=request.POST.get('employee_age',None)
        phone=request.POST.get('employee_phone',None)
        designation=request.POST.get('employee_designation',None)
        department=request.POST.get('employee_department',None)

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
        'designation_choices':Employee.designation_choices,
        'department_choices':Employee.department_choices
    }

    return render(request, 'add_employee.html', context)


def add_project(request):
    if request.method=='POST':
        name=request.POST.get('project_name', None)
        date_of_receive=request.POST.get('project_date_of_receive',None)
        duration=request.POST.get('project_duration',None)
        department=request.POST.get('project_department',None)
        hours=request.POST.get('project_hours',None)
        
       
        project=Project.objects.create(
            name=name,
            date_of_receive=date_of_receive,
            duration=duration,
            department=department,
            hours=hours  
            )
        
        project.save()

        return redirect('adminpage')
    
    context={
        'department_choices':Project.department_choices
    }

    return render(request, 'add_project.html', context)

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