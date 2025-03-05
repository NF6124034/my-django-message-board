from django.urls import path
from .views import message_list, delete_message, edit_message,register,like_message,profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', message_list, name='message_list'),
    path('delete/<int:id>/', delete_message, name='delete_message'),
    path('edit/<int:id>/', edit_message, name='edit_message'),
    path('login/', auth_views.LoginView.as_view(template_name='board/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    path('like/<int:id>/', like_message, name='like_message'),
    path('profile/', profile, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='board/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='board/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='board/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='board/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='board/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='board/password_reset_complete.html'), name='password_reset_complete'),
]
