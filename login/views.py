from django.shortcuts import render, redirect
from django.contrib import messages
from . models import User, Job
import bcrypt


def index(request):
    return render(request, "login.html")

def registration_form(request):
    errors =  User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            username = request.POST['username'],
            password = pw_hash
        )
        messages.error(request, "Created Account, please log in")
        return redirect('/')

def login(request):
    users = User.objects.filter(username = request.POST['username'])
    if len(users) != 1:
        messages.error(request, "No user with given username in database")
        return redirect('/')

    user = users[0]

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Password does not match")
        return redirect('/')

    request.session['user_id'] = user.id
    request.session['user_username'] = user.username
    request.session['user_email'] = user.email
    return redirect('/dashboard')

def dashboard(request):
    context = {
        'all_jobs': Job.objects.all()
    }
    if not 'user_id' in request.session:
        messages.error(request, 'Please log in to view this page')
        return redirect('/')

    return render(request, 'dashboard.html', context)

def logout (request):
    del request.session['user_id']
    del request.session['user_username']
    del request.session['user_email']

    return redirect('/')

def create_a_job(request):
    return render(request, "create_new_job.html")

def create_a_job_form(request):
    errors =  Job.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/new')
    else:
        Job.objects.create(
        title = request.POST["title"], 
        desc = request.POST["desc"], 
        location = request.POST["location"],
        creator = User.objects.get(id = request.session['user_id'])
        )

    return redirect("/dashboard")

def show_individual_job_info(request, job_id):
    context = {
        'job': Job.objects.get(id= job_id)
    }

    return render(request, 'display_job.html', context)

def display_form_to_edit_job_id(request, job_id):
    context = {
        'job': Job.objects.get(id= job_id)
    }
    return render(request, 'edit_the_job.html', context)

def submit_form_to_edit_your_job(request, job_id):
    errors =  Job.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/job/{job_id}/edit')
    else:
        creator = User.objects.get(id = request.session['user_id'])
        edit_job = Job.objects.get(id=job_id)
        edit_job.title = request.POST["title"]
        edit_job.desc = request.POST["desc"]
        edit_job.location = request.POST["location"]
        edit_job.save()
    
    return redirect('/dashboard')

def delete_job(request, job_id):
    creator = User.objects.get(id = request.session['user_id'])
    delete_job = Job.objects.get(id= job_id)
    delete_job.delete()

    return redirect("/dashboard")