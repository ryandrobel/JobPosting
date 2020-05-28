from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index), 
    path('register', views.registration_form),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('jobs/new', views.create_a_job),
    path('create_job', views.create_a_job_form),
    path('job/<job_id>', views.show_individual_job_info),
    path('job/<job_id>/edit', views.display_form_to_edit_job_id),
    path('edit_job/<job_id>', views.submit_form_to_edit_your_job),
    path('job/<job_id>/delete', views.delete_job),
]