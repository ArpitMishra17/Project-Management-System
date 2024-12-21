from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('adminpage/',views.adminpage,name='adminpage'),
    path('add_employee/',views.add_employee,name="add_employee"),
]