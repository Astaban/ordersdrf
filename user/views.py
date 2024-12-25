from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from user.forms import UserLoginForm, ProfileUserForm, UserPasswordChangeForm


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user:login'))


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse_lazy('courses_list')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'user/profile.html'
    extra_context = {'title': 'Профиль'}

    def get_success_url(self):
        return reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("user:password_change_done")
    template_name = "registration/password_change_form.html"


# class RegisterUser(CreateView):
#     form_class = UserRegisterForm
#     template_name = 'users/registration.html'
#     success_url = reverse_lazy('users:login')
#     extra_context = {'title': 'Регистрация пользователя'}


