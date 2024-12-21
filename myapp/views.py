from django.shortcuts import render, redirect,get_object_or_404
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