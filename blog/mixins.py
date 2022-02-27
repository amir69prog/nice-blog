from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render


class UserVerifiedPermission(UserPassesTestMixin):
    def custom_handle_no_permission(self):
        return render(self.request, 'accounts/unverified_user.html')

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.custom_handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_verified


class IsAuthorAndVerifiedPermission(UserPassesTestMixin):
    def custom_handle_no_permission(self):
        return render(self.request, 'accounts/author_not_user.html')

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.custom_handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author and self.request.user.is_verified
