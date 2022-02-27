from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .models import Post
from .mixins import UserVerifiedPermission, IsAuthorAndVerifiedPermission
from .messages import PostMessages 


class PostListView(LoginRequiredMixin,
                    UserVerifiedPermission, ListView):
    login_url = '/accounts/login/'
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 20


class PostDetailView(LoginRequiredMixin,
                    UserVerifiedPermission, DetailView):
    login_url = '/accounts/login/'
    model = Post
    template_name = 'blog/post.html'


class CreatePostView(LoginRequiredMixin,
                    UserVerifiedPermission, CreateView):
    login_url = '/accounts/login/'
    model = Post
    fields = ('title', 'subheading', 'body', 'reading_time')
    template_name = 'blog/create_post.html'

    def form_valid(self, form):
        """ When submitting form if that valid author will set for this post """
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.SUCCESS, PostMessages.POST_CREATED_SUCCESSFULLY.value)
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin,
                    IsAuthorAndVerifiedPermission,
                    DeleteView):
    login_url = '/accounts/login/' 
    model = Post
    template_name = 'blog/delete_post.html'

    def form_valid(self, form):
        """ When submitting form if that valid author will set for this post """
        messages.add_message(self.request, messages.SUCCESS, PostMessages.POST_DELETED_SUCCESSFULLY.value)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('accounts:profile')


class UpdatePostView(LoginRequiredMixin,
                    IsAuthorAndVerifiedPermission,
                    UpdateView):
    login_url = '/accounts/login/'
    model = Post
    fields = ('title', 'subheading', 'body', 'reading_time')
    template_name = 'blog/update_post.html'

    def form_valid(self, form):
        """ When submitting form if that valid adding message """
        messages.add_message(self.request, messages.SUCCESS, PostMessages.POST_UPDATED_SUCCESSFULLY.value)
        return super().form_valid(form)