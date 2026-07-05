from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy

from accounts.models import Follow
from posts.forms import PostForm, CommentForm
from posts.models import Post, Like, Comment


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'posts/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        following_users = Follow.objects.filter(
            follower=self.request.user
        ).values_list('following', flat=True)
        return Post.objects.filter(
            author__in=following_users
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        liked_posts = Like.objects.filter(
            user=self.request.user
        ).values_list('post_id', flat=True)
        context['liked_posts'] = set(liked_posts)
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.order_by('created_at')
        context['is_liked'] = Like.objects.filter(
            user=self.request.user,
            post=self.object
        ).exists()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        self.request.user.profile.posts_count += 1
        self.request.user.profile.save()
        return redirect('posts:post_detail', pk=post.pk)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def form_valid(self, form):
        self.request.user.profile.posts_count -= 1
        self.request.user.profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'pk': self.request.user.pk})


class LikeView(LoginRequiredMixin, DetailView):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )
        if created:
            post.likes_count += 1
            post.save()
        return redirect('posts:post_detail', pk=pk)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = post
        comment.save()
        post.comments_count += 1
        post.save()
        return redirect('posts:post_detail', pk=post.pk)