
from django.urls import include, path

from users.views import RegisterView


urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
]