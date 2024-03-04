from django.urls import path
from django.contrib.auth import views as auth_views
from .views import reset_views,user_views

app_name = 'common'

urlpatterns = [
    path('my_page/', user_views.mypage, name='mypage'),
    path('profile/', user_views.profile, name='profile'),
    path('profile_update/', user_views.profile_update, name='profile_update'),
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('signup/', user_views.signup, name='signup'),
    path('update/', user_views.update, name='update'),
    path('modify_password/', user_views.modify_password, name='modify_password'),
    path('delete/', user_views.delete, name='delete'),

    path('password_reset', reset_views.UserPasswordResetView.as_view()),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(template_name='common/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', reset_views.UserPasswordResetConfirmView.as_view(template_name='common/set_password.html'), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='common/set_password_done.html'), name="password_reset_complete"),
]