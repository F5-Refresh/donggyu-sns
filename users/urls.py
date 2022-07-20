from django.urls import path

from users.views import UserSignUpView, UserSignInView


"""
유저 회원가입/로그인/로그아웃 url patterns
"""
urlpatterns = [
    path('/signup', UserSignUpView.as_view()),
    path('/signin', UserSignInView.as_view()),
]