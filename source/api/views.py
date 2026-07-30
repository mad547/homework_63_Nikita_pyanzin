from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from posts.models import Post, Like, Comment
from api.serializers import PostSerializer, LikeSerializer, CommentSerializer


class IsAuthorOrReadOnly:
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrReadOnly()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        self.request.user.profile.posts_count += 1
        self.request.user.profile.save()

    def perform_destroy(self, instance):
        instance.author.profile.posts_count -= 1
        instance.author.profile.save()
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )
        if created:
            post.likes_count += 1
            post.save()
            return Response({'liked': True, 'likes_count': post.likes_count}, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            post.likes_count -= 1
            post.save()
            return Response({'liked': False, 'likes_count': post.likes_count}, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrReadOnly()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs.get('post_pk'))
        comment = serializer.save(author=self.request.user, post=post)
        post.comments_count += 1
        post.save()

    def perform_destroy(self, instance):
        instance.post.comments_count -= 1
        instance.post.save()
        instance.delete()