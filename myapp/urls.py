from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('',views.employee_login,name='employee_login'),
    path('adminpage/',views.adminpage,name='adminpage'),
    path('add_employee/',views.add_employee,name="add_employee"),
    path('add_project',views.add_project,name="add_project"),
    path('display_employees',views.display_employees,name="display_employees"),
    path('display_projects',views.display_projects,name='display_projects'),
    path('add_department',views.add_department,name="add_department"),
    path('add_designation',views.add_designation,name="add_designation"),
    path('display_departments',views.display_departments,name='display_departments'),
    path('display_designations',views.display_designations,name='display_designations'),
    path('add_project_department',views.add_project_department,name="add_project_department"),
    path('display_project_departments',views.display_project_departments,name='display_project_departments'),
    path('project_home/<int:project_id>',views.project_home,name="project_home"),
    path('manager_home/',views.manager_home,name="manager_home"),
    path('test_employee/',views.test_employee,name="test_employee"),
    path("manager_project_home<int:project_id>/",views.manager_project_home,name="manager_project_home"),
    path('get_employees_by_designation', views.get_employees_by_designation, name='get_employees_by_designation'),
]