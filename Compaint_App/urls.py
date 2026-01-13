from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('submit_complaint/', views.submit_complaint, name='submit_complaint'),
    path('my-complaints/', views.view_student_complaints, name='view_student_complaints'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view_admin_complaints/', views.view_admin_complaints, name='view_admin_complaints'),
    path('admin_response/<int:complaint_id>/', views.admin_response, name='admin_response'),
    
]
