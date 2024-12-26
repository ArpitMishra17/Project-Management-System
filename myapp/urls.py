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
    path('employee_home/',views.employee_home,name="employee_home"),
    path("manager_project_home<int:project_id>/",views.manager_project_home,name="manager_project_home"),
    path('get_employees_by_designation', views.get_employees_by_designation, name='get_employees_by_designation'),
    path('add_task/<int:project_id>/', views.add_task, name='add_task'),
    path('add_module/<int:project_id>/',views.add_module,name='add_module'),
    path('start_task/<int:task_id>', views.start_task, name='start_task'),
    path('stop_task/<int:task_id>', views.stop_task, name='stop_task'),
    path('update-password/', views.update_password, name='update_password'),
]