from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views

# The following is a list of all the paths that are available to the user for the accounts app.
urlpatterns = [
    # register
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.view_user, name='view_user'),
    path('profile/<int:user_id>/message/', views.send_pm, name='send_pm'),
    path('messages/', views.view_messages, name='view_pms'),
    path('messages/view_message/<int:message_id>/', views.view_message, name='view_pm'),
    # login (django.contrib.auth.views.LoginView)
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # logout (django.contrib.auth.views.LogoutView)
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    # password_change (django.contrib.auth.views.PasswordChangeView)
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),
    # password_change_done (django.contrib.auth.views.PasswordChangeDoneView)
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
    # password_reset (django.contrib.auth.views.PasswordResetView)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='password_reset'),
    # password_reset_done (django.contrib.auth.views.PasswordResetDoneView)
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    # password_reset_confirm (django.contrib.auth.views.PasswordResetConfirmView)
    path('password_reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    # password_reset_complete (django.contrib.auth.views.PasswordResetCompleteView)
    path('password_reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]
