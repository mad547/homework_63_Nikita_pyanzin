from django.urls import path
from accounts.views import (
    CustomLoginView, RegisterView, ProfileView,
    ProfileEditView, UserSearchView, FollowView
)
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('<int:pk>/follow/', FollowView.as_view(), name='follow'),
]