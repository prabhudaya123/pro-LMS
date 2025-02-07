# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Video(models.Model):
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')  # The file will be stored in 'MEDIA_ROOT/documents/'
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    marks = models.IntegerField(default=1)  # Ensure this field exists in your model
    # Add any other fields here

    def __str__(self):
        return self.title

class Question(models.Model):
    question_text = models.TextField()
    marks = models.IntegerField(default=1)
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default="A")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return f"Question {self.id} for {self.quiz.title}"

class Option(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    option_a = models.CharField(max_length=255, default="Default Option")
    option_b = models.CharField(max_length=255, default="Default Option")
    option_c = models.CharField(max_length=255, default="Default Option")
    option_d = models.CharField(max_length=255, default="Default Option")
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default="A")

    def __str__(self):
        return f"Options for: {self.question.question_text}"


class StudentAnswer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Update to reference the custom user model
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer by {self.student} for {self.question}"


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username