from django.contrib import admin
from .models import Video,Document,Quiz, Question, Option

from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_file']
admin.site.register(Document)


 

# Register Quiz model
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # Adjust this according to your model fields

# Register Question model
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'marks', 'quiz')     # Use actual field names from the Question model

# Register Option model
@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'option_a', 'option_b', 'option_c', 'option_d')  # Adjust this according to your Option model fields
