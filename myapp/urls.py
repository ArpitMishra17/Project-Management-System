from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('adminpage/',views.adminpage,name='adminpage'),
    path('add_employee/',views.add_employee,name="add_employee"),
    path('add_project',views.add_project,name="add_project"),
    path('display_employees',views.display_employees,name="display_employees"),
    path('display_projects',views.display_projects,name='display_projects')
]