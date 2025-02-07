from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('upload-document/', views.upload_document, name='upload_document'),
    path('document-list/', views.document_list, name='document_list'),
    path('view_all/',views.view_all,name='view_all'),
    path('add_content/',views.add_content,name='add_content'),

    path('upload-videos/', views.upload_videos, name='upload_videos'),
    path('video-list/', views.video_list, name='video_list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
