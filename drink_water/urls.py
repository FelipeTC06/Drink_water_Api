from django.urls import include, path

urlpatterns = [
    path('user_auth/', include('user_auth.urls')),
]
