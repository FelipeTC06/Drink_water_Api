from django.urls import path
from . import views

urlpatterns = [
    path('register-intake/', views.register_intake, name='register-intake'),
    path('daily-progress/<int:user_id>/', views.daily_progress, name='daily-progress'),
    path('intake-history/<int:user_id>/', views.intake_history, name='intake-history'),
]
