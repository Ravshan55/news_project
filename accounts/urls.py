from django.contrib.auth.views import LoginView, LogoutView
from django.views import View

from .views import LogoutConfirmView, EditUserView
from django.urls import path
from .views import dashboard_view, user_register, edit_user
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView





urlpatterns = [
    # path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutConfirmView.as_view(), name='logout_page'),  # GET — shows the confirm page
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('passord_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', dashboard_view, name='user_profile'),
    path('signup/', user_register, name='user_register'),
    # path('profile/edit/', EditUserView.as_view(), name='edit_user_information'),
    path('profile/edit/', edit_user, name='edit_user_information'),
    # path('signup/', SignUpView.as_view(), name='user_register')



]
