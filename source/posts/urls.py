from django.urls import path
from posts.views import (
    IndexView, PostDetailView, PostCreateView,
    PostDeleteView, LikeView, CommentCreateView
)

app_name = 'posts'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/like/', LikeView.as_view(), name='like'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
]