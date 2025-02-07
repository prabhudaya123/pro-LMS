from django import forms
from django.forms import modelformset_factory
from .models import Video, Document, Quiz  # Import models from models.py

# Video Form
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']

# Create a formset for Video
VideoFormSet = modelformset_factory(Video, form=VideoForm, extra=1)

# Document Form
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'marks']  # Include the fields you want in the form
