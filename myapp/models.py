from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import timedelta,datetime,time
from django.core.exceptions import ValidationError

# Create your models here.


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email ,password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email,password, **other_fields)

    def create_user(self,email, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email'))

        email = self.normalize_email(email)
        user = self.model( email=email,
                        **other_fields)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user
    
class Employee(AbstractBaseUser, PermissionsMixin):

    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128, default="password", blank=True)

    projects=models.ManyToManyField("Project",related_name="employees")

    tasks=models.ManyToManyField("Task",related_name="employees")



    designation=models.ForeignKey("Designation",on_delete=models.SET_NULL,null=True)
    department=models.ForeignKey("Department",on_delete=models.SET_NULL,null=True)

    # Permissions fields
    is_staff = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    

    # Manager
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    
    

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_"):
            self.set_password(self.password)  # Automatically hash the password
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.email)
    

class Project(models.Model):

    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    date_of_receive=models.DateField(null=True, blank=True)
    duration=models.IntegerField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True, editable=False) 
   

    project_department=models.ForeignKey("projectDepartment",on_delete=models.SET_NULL,null=True)
    hours=models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
       
        if self.date_of_receive and self.duration is not None:
            self.deadline = self.date_of_receive + timedelta(days=self.duration)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
    

class Department(models.Model):

    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}" 
    
class Designation(models.Model):

    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}" 
    
class projectDepartment(models.Model):

    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}" 
    

    

class Module(models.Model):

    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    project_id=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    estimated_duration=models.IntegerField(null=True,blank=True)
    start_time=models.DateTimeField(null=True,blank=True)
    end_time=models.DateTimeField(null=True,blank=True)
    actual_duration=models.IntegerField(null=True,blank=True)
    description=models.CharField(max_length=200,null=True,blank=True)
    status_choices=(
        ("Not started","Not started"),
        ("Ongoing","Ongoing"),
        ("Finished","Finished")
    )
    status=models.CharField(max_length=100,choices=status_choices,default="Not started")

    
    def __str__(self):
        return f"{self.name}" 
    

class Task(models.Model):

    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    
    module_id=models.ForeignKey(Module,on_delete=models.CASCADE,null=True,blank=True, related_name="tasks")
    estimated_duration=models.IntegerField(null=True,blank=True)
    start_time=models.DateTimeField(null=True,blank=True)
    end_time=models.DateTimeField(null=True,blank=True)
    actual_duration=models.IntegerField(null=True,blank=True)
    description=models.CharField(max_length=200,null=True,blank=True)
    status_choices=(
        ("Not started","Not started"),
        ("Ongoing","Ongoing"),
        ("Finished","Finished")
    )
    status=models.CharField(max_length=100,choices=status_choices,default="Not started")
    priority_choices=(
        ("High Priority","High Priority"),
        ("Medium Priority","Medium Priority"),
        ("Low Priority","Low Priority")
    )
    priority=models.CharField(max_length=100,choices=priority_choices,default="Low Priority")

    def calculate_duration(self):
        if not (self.start_time and self.end_time):
            return 0
        
        if self.start_time > self.end_time:
            raise ValidationError("Start time must be before end time")
            
        duration = self.end_time - self.start_time
        return duration.total_seconds() / 3600
    
    def update_project_hours(self, duration):
        if self.module_id and self.module_id.project_id:
            project = self.module_id.project_id
            if project.hours is not None:  # Check if hours is not None
                project.hours = max(0, project.hours - duration)  # Ensure hours don't go negative
                project.save()
    
    def update_module_times(self):
        if not self.module_id:
            return

        module = self.module_id
        all_tasks = module.tasks.all()
        
        # Update module start time when first task starts
        if self.status == "Ongoing" and self.start_time:
            started_tasks = all_tasks.exclude(id=self.id).filter(start_time__isnull=False)
            if not started_tasks.exists():
                # This is the first task to start
                module.start_time = self.start_time
                module.status = "Ongoing"
        
        # Update module end time when last task finishes
        if self.status == "Finished":
            unfinished_tasks = all_tasks.exclude(id=self.id).filter(
                status__in=["Not started", "Ongoing"]
            )
            if not unfinished_tasks.exists():
                # This was the last task to finish
                module.end_time = self.end_time
                module.status = "Finished"
                
                # Calculate module's actual duration
                if module.start_time and module.end_time:
                    duration = module.end_time - module.start_time
                    module.actual_duration = duration.total_seconds() / 3600

        module.save()


    def save(self, *args, **kwargs):
        is_new_finish = False
        if self.pk:  # If task already exists
            old_task = Task.objects.get(pk=self.pk)
            # Check if task is being marked as finished for the first time
            is_new_finish = old_task.status != "Finished" and self.status == "Finished"
        else:
            is_new_finish = self.status == "Finished"


        if self.status == "Finished" and self.start_time and self.end_time:
            self.actual_duration = self.calculate_duration()

            if is_new_finish:
                self.update_project_hours(self.actual_duration)
            
            # Get the project through the module
            if self.module_id and self.module_id.project_id:
                project = self.module_id.project_id
                
                # Update hours for each assigned employee
                for employee in self.employees.all():
                    hours_record, created = EmployeeProjectHours.objects.get_or_create(
                        employee=employee,
                        project=project
                    )
                    hours_record.total_hours += self.actual_duration
                    hours_record.save()
        
        super().save(*args, **kwargs)

        self.update_module_times()

    def __str__(self):
        return f"{self.name}" 
    

class EmployeeProjectHours(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    total_hours = models.FloatField(default=0)

    class Meta:
        unique_together = ('employee', 'project')

    def __str__(self):
        return f"{self.employee.name} - {self.project.name} - {self.total_hours} hours"
    

class Todo(models.Model):
    id=models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']