from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Video,Document,Quiz, Question, Option
from .forms import VideoFormSet,DocumentForm
from django.http import JsonResponse
from .forms import QuizForm
import os
from .models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .decorators import role_required
from django.contrib.auth.decorators import login_required


# Registration view
def home(request):
    return render(request, 'home.html')
def add_content(request):
    return render(request,'add_content.html')
def view_all(request):
    return render(request,'view_all.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email_id = request.POST.get('email_id', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_no = request.POST.get('phone_no', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', '')

        # Ensure required fields are not empty
        if not username or not email_id or not password or not confirm_password:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'register.html')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        # Save user
        try:
            user = User.objects.create_user(
                username=username,
                email=email_id,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            user.role = role
            user.phone_no = phone_no  # Optional field
            user.date_of_birth = date_of_birth  # Optional field
            user.save()
            messages.success(request, "Registration successful!")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, 'register.html')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
    return render(request, 'login.html')

@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')

@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')



""" Documents"""


def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_document')  # Redirect to the list view after successful upload
    else:
        form = DocumentForm()

    return render(request, 'upload_document.html', {'form': form})

def document_list(request):
    documents = Document.objects.all()

    # Add file extension as metadata for each document
    for doc in documents:
        doc.file_extension = os.path.splitext(doc.file.url)[-1].lower()  # e.g., '.pdf', '.jpg'
    
    return render(request, 'document_list.html', {'documents': documents})
""" video"""
def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def upload_videos(request):
    if request.method == 'POST':
        formset = VideoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            messages.info(request, '*Upload successfully done*')
            #return redirect('pload_videos')  # Ensure this matches the name in urls.py
    else:
        formset = VideoFormSet(queryset=Video.objects.none())

    return render(request, 'upload_videos.html', {'formset': formset})

