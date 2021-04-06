from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='home'),
    path('category/<str:slug>/', get_category, name='category'),
    path('watch/<str:slug>/', view_film, name='view_film'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('', index, name='home'),

    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name='activate'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
         name='password_reset_complete'),
]
