from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api.views import PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

app_name = 'api_instagram'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api-login'),
]