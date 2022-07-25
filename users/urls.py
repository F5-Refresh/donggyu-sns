from django.urls import path
from users.views import UserSignUpView, UserSignInView, UserSignOutView

from rest_framework_simplejwt.views import TokenRefreshView


"""
유저 회원가입/로그인/로그아웃 url patterns
"""
urlpatterns = [
    path('/signup', UserSignUpView.as_view()),
    path('/signin', UserSignInView.as_view()),
    path('/signout', UserSignOutView.as_view()),
]

"""
유저 토큰 리프레시(재로그인 기능) url patterns
detail: 리프레시 토큰으로 다시 로그인을 시도하면 액세스 토큰을 재발급(리프레시 토큰 재발급X)
"""
urlpatterns += [
    path('/token/refresh', TokenRefreshView.as_view()),
]