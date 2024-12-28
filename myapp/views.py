from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from .models import Employee,Project,Department,Designation,projectDepartment,Task,Module
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password
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
                return redirect("employee_home")
        else:
            
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    

    return render(request, 'login.html')

def update_password(request):
    employee=request.user
    referer = request.GET.get('referer', 'employee_home') 

    if request.method=='POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not check_password(current_password, employee.password):
            messages.error(request, "Current password is incorrect.")
            return redirect('update_password')
        
        if new_password != confirm_password:
            messages.error(request, "New password and confirmation do not match.")
            return redirect('update_password')
        
        employee.password = make_password(new_password)
        employee.save()

        login(request, employee)
        messages.success(request, "Password updated successfully!")
        return redirect(referer)
        
    return render(request, 'update_password.html', {'referer': referer})


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
            return redirect('display_projects')
        
        

    context={
        'employees':employees,
        'project':project
    }

    return render(request,'project_home.html',context)

def employee_home(request):

    employee=Employee.objects.get(email=request.user.email)

    return render(request,'employee_home.html',{'employee':employee})

def manager_home(request):

    employee=Employee.objects.get(email=request.user.email)
    projects = employee.projects.all()

    
    # Gather all tasks related to the manager's projects
    tasks = Task.objects.filter(module_id__project_id__in=projects).select_related('module_id', 'module_id__project_id').prefetch_related('employees')

    project_tasks_list = []

    for project in projects:
        project_tasks = tasks.filter(module_id__project_id=project)
        
        for task in project_tasks:
            project_tasks_list.append(
            {
                "task_name" : task.name,
                "project_name" : project.name,
                "module_name" : task.module_id.name,
                "employee_names": [employee.name for employee in task.employees.all()],
                "task_status" : task.status,
                "task_priority" : task.priority,
                "task_endTime" : task.end_time,
                
            }
            )

    context={
        'project_tasks_list': project_tasks_list,
        'employee':employee,
        
    }


    return render(request,'manager_home.html',context)




def manager_project_home(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    designations = Designation.objects.all()

    if request.method == "POST":
        designation = request.POST.get('designation')
        employee_id = request.POST.get('employee')

        if employee_id:
            employee = get_object_or_404(Employee, id=employee_id)
            project.employees.add(employee)
            return redirect('manager_project_home', project_id=project.id)

    # Get all modules with their tasks
    modules = project.module_set.all().prefetch_related('tasks')
    
    # Get unassigned employees
    unassigned_employees = Employee.objects.exclude(
        id__in=project.employees.values_list('id', flat=True)
    )

    context = {
        'project': project,
        'designations': designations,
        'employees': unassigned_employees,
        'modules': modules,
    }

    return render(request, 'manager_project_home.html', context)

def get_employees_by_designation(request):
    designation=request.GET.get('designation')
    project_id = request.GET.get('project_id')

    project = get_object_or_404(Project, id=project_id)
    employees = Employee.objects.filter(designation=designation).exclude(
        id__in=project.employees.values_list('id', flat=True)
    ).values('id', 'name')
    return JsonResponse(list(employees),safe=False)

def add_module(request,project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)

        
        module_name = request.POST.get('module_name')
        estimated_duration = request.POST.get('estimated_duration')
        description = request.POST.get('description')
       

       
        if not module_name:
            messages.error(request, "Please provide the module name.")
            return redirect('manager_project_home', project_id=project_id)

   
        Module.objects.create(
            name=module_name,
            project_id=project,
            estimated_duration=estimated_duration,
            description=description
        )

        messages.success(request, "Module added successfully!")
        return redirect('manager_project_home', project_id=project_id)

    return redirect('manager_project_home', project_id=project_id)

def add_task(request, project_id):
    if request.method == 'POST':
       
        project = get_object_or_404(Project, id=project_id)
        print("project id" , project_id)
        print("project id ---" , project.id)
        print("project name ---" , project.name)

        task_name = request.POST.get('task_name')
        employee_id = request.POST.get('task_employee')
        module_id = request.POST.get('task_module')
        print("module_id" , module_id)

      
        employee = get_object_or_404(Employee, id=employee_id)
        module = get_object_or_404(Module, id=module_id, project_id=project)
        print("module_id from db" , module.id)
        
        estimated_duration = request.POST.get('estimated_duration')
        priority = request.POST.get('priority')

    
        task = Task.objects.create(
            name=task_name,
            module_id=module,
            description=request.POST.get('description'),
            estimated_duration=estimated_duration,
            priority=priority,
        )

        task.employees.add(employee)
        task.module_id = module  
        
        task.save() 
        print("task id" , task.id)          


        messages.success(request, "Task added successfully!")
        return redirect('manager_project_home', project_id=project_id)

    return redirect('manager_project_home', project_id=project_id)



# View to start a task (change status to Ongoing and set start time)
def start_task(request,task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.status == "Not started":
        task.start_time = timezone.now().time()
        task.status = "Ongoing"
        task.save()
        messages.success(request, "Task started successfully!")
    else:
        messages.error(request, "Task cannot be started.")

    return redirect('employee_home')  # Redirect after starting the task
# View to stop a task (set stop time and change status to 'Finished')
def stop_task(request,task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.status == "Ongoing":
        task.end_time = timezone.now().time()
        task.status = "Finished"
        task.save()
        messages.success(request, "Task ended successfully!")
    else:
        messages.error(request, "Task cannot be ended.")

    return redirect('employee_home') 

def display_modules(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    modules = project.module_set.all()

    context = {
        'project': project,
        'modules': modules,
    }
    return render(request, 'display_modules.html', context)


def display_tasks(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    modules = project.module_set.prefetch_related('tasks')

    tasks = []
    for module in modules:
        tasks.extend(module.tasks.all())

    context = {
        'project': project,
        'tasks': tasks,
    }
    return render(request, 'display_tasks.html', context)