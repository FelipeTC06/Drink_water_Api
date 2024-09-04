from django.urls import include, path

urlpatterns = [
    path('user_auth/', include('user_auth.urls')),
    path('water_tracking/', include('water_tracking.urls')),
]
