from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from accounts.forms import RegisterForm, ProfileForm, ProfileEditForm, LoginForm
from accounts.models import Profile, Follow


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username_or_email = form.cleaned_data.get('username_or_email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username_or_email, password=password)
        if user is None:
            try:
                user_obj = get_user_model().objects.get(email=username_or_email)
                user = authenticate(self.request, username=user_obj.username, password=password)
            except get_user_model().DoesNotExist:
                pass
        if user is not None:
            login(self.request, user)
            return redirect('posts:index')
        form.add_error(None, 'Неверный логин/email или пароль')
        return self.form_invalid(form)


class RegisterView(CreateView):
    model = get_user_model()
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in kwargs:
            context['profile_form'] = ProfileForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile_form.instance = profile
            profile_form.save()
            login(request, user)
            return redirect('accounts:profile', pk=user.pk)
        return self.render_to_response(
            self.get_context_data(form=form, profile_form=profile_form)
        )


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        context['posts'] = profile_user.posts.all()
        context['is_following'] = Follow.objects.filter(
            follower=self.request.user,
            following=profile_user
        ).exists()
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'accounts/profile_edit.html'
    form_class = ProfileEditForm
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in kwargs:
            context['profile_form'] = ProfileForm(instance=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect('accounts:profile', pk=request.user.pk)
        return self.render_to_response(
            self.get_context_data(form=form, profile_form=profile_form)
        )


class UserSearchView(LoginRequiredMixin, ListView):
    template_name = 'accounts/search.html'
    context_object_name = 'users'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return get_user_model().objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query)
            ).exclude(pk=self.request.user.pk)
        return get_user_model().objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class FollowView(LoginRequiredMixin, DetailView):
    def post(self, request, pk):
        user_to_follow = get_object_or_404(get_user_model(), pk=pk)
        if user_to_follow == request.user:
            return redirect('accounts:profile', pk=pk)
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        if created:
            user_to_follow.profile.followers_count += 1
            user_to_follow.profile.save()
            request.user.profile.following_count += 1
            request.user.profile.save()
        else:
            follow.delete()
            user_to_follow.profile.followers_count -= 1
            user_to_follow.profile.save()
            request.user.profile.following_count -= 1
            request.user.profile.save()
        return redirect('accounts:profile', pk=pk)