from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('user/', user_dashboard, name='user_dashboard'),
     path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
 

]
