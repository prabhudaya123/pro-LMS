from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.contrib import messages


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

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
