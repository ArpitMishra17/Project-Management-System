from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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



    project_department=models.ForeignKey("projectDepartment",on_delete=models.SET_NULL,null=True)
    hours=models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
       
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