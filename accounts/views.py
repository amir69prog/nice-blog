from audioop import reverse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView

from accounts.models import CustomUser

from .messages import UserMessage
from api.users.messages import ViewMessages
from .forms import UserProfileForm, CustomUserCreationForm


@login_required
def user_profile_view(request: HttpRequest) -> HttpResponse:
    form = UserProfileForm(instance=request.user)

    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            text = UserMessage.PROFILE_UPDATED_SUCCESSFULLY.value
            messages.add_message(request, messages.SUCCESS, text)
            return redirect(request.path_info)
        else:
            text = ViewMessages.SOMETHING_WENT_WRONG.value
            messages.add_message(request, messages.WARNING, text)
            form = UserProfileForm(instance=request.user, data=request.POST)

    context = {
        'form': form
    }
    return render(request, 'accounts/profile.html', context)


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    
    def get_success_url(self) -> str:
        return reverse('login')