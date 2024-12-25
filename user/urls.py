from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from user import views

app_name = 'user'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    path(
        'password-reset/',
        PasswordResetView.as_view(
            success_url=reverse_lazy('users:password_reset_done'),
            email_template_name='users/password_reset_email.html'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'password-reset/<uidb64>/<token>',
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('users:password_reset_complete')),
        name='password_reset_confirm'
    ),
    path(
        'password-reset/complete/',
        PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),

]