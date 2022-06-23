
from django.urls import include, path

from users.views import RegisterView


urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    #  dj_rest_auth package urls login/logout/password/reset/confirm/set_password
    path('register/', RegisterView.as_view(), name='register'),
    # standart rest framework auth urls for login/logout
    path('api-auth/', include('rest_framework.urls'))
]