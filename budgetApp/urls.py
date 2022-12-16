from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('signup_page/', signup_page, name='signup_page'),
    path('otp_page/', otp_page, name='otp_page'),
    path('signin_page/', signin_page, name='signin_page'),
    path('profile_page/', profile_page, name='profile_page'),
    path('forgot_pwd_page/', forgot_pwd_page, name='forgot_pwd_page'),

    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('profile_update/', profile_update, name='profile_update'),
    path('password_reset/', password_reset, name='password_reset'),
    path('verify_otp/<str:verify_for>/', verify_otp, name='verify_otp'),

    path('add_budget/', add_budget, name='add_budget'),
    path('add_expsense/', add_expsense, name='add_expsense'),

    path('logout/', logout, name='logout'),
]