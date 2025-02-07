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




def create_quiz(request):
    if request.method == 'POST':
        quiz_title = request.POST.get('quiz_title')
        quiz_description = request.POST.get('quiz_description')
        quiz = Quiz.objects.create(title=quiz_title, description=quiz_description)

        questions = request.POST.getlist('question[]')
        options = request.POST.getlist('option[]')
        correct_options = request.POST.getlist('correct_option[]')  # Now correct option is A, B, C, D

        for i, question_text in enumerate(questions):
            # Create Question object without options
            question = Question.objects.create(
                quiz=quiz,
                question_text=question_text,
                marks=1  # You can adjust the marks as needed
            )

            # Get options for the current question
            option_a = options[i * 4 + 0] if options[i * 4 + 0] else "Default Option A"
            option_b = options[i * 4 + 1] if options[i * 4 + 1] else "Default Option B"
            option_c = options[i * 4 + 2] if options[i * 4 + 2] else "Default Option C"
            option_d = options[i * 4 + 3] if options[i * 4 + 3] else "Default Option D"
            correct_option = correct_options[i]  # 'A', 'B', 'C', 'D'

            # Create Option object and associate it with the current question
            Option.objects.create(
                question=question,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_option=correct_option  # No need to convert
            )

        return redirect('quiz_list')

    return render(request, 'create_quiz.html')

    
def attempt_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Get all the questions for this quiz

    # Fetch options for each question
    for question in questions:
        question.options = question.option_set.all()  # Fetch related options for the question
    
    if request.method == 'POST':
        score = 0
        total_marks = 0 
        for question in questions:
            selected_answer = request.POST.get(f"question_{question.id}")  # Selected answer from form
            
            # Fetch the correct option from the associated options
            correct_option_obj = question.option_set.first()  # Get the first option
            if selected_answer.upper() == correct_option_obj.correct_option.upper():
                score += question.marks
            total_marks += question.marks
        percentage = (score / total_marks) * 100 if total_marks > 0 else 0
        percentage = round(percentage, 2)
        return render(request, 'submit_quiz.html', {'score': score, 'quiz': quiz,'percentage': percentage,'total_marks': total_marks})

    return render(request, 'attempt_quiz.html', {'quiz': quiz, 'questions': questions})






def quiz_list(request):
    quizzes = Quiz.objects.all()  # Get all quizzes from the database
    return render(request, 'quiz_list.html', {'quizzes': quizzes})


def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    score = 0
    total_marks = 0  # Initialize total_marks

    for question in questions:
        selected_answer = request.POST.get(f"question_{question.id}")  # 'A', 'B', 'C', or 'D'
        
        # Fetch the correct answer from the `Option` model
        correct_answer = question.option_set.first().correct_option  # Already stored as 'A', 'B', 'C', 'D'

        if selected_answer == correct_answer:
            score += question.marks
        
        total_marks += question.marks  # Add to total_marks

    percentage = (score / total_marks) * 100 if total_marks > 0 else 0
    percentage = round(percentage, 2)  # Round the percentage to 2 decimal places

    # Print to check if values are passed correctly
    print(f"Score: {score}, Total Marks: {total_marks}, Percentage: {percentage}")

    return render(request, 'submit_quiz.html', {
        'score': score,
        'quiz': quiz,
        'percentage': percentage,  # Pass the calculated percentage
        'total_marks': total_marks  # Pass total_marks to show in the template
    })



