from django.urls import path
from .views import MeView, GoogleAuthView, LogoutView

urlpatterns = [
    path('me/', MeView.as_view(), name='user-me'),
    path('google/', GoogleAuthView.as_view(), name='google-auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
]