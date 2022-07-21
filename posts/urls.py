from django.urls import path

from posts.views import PostView, PostDetailView, PostRestoreView, PostLikeView


"""
게시물 url patterns
"""
urlpatterns = [
    path('', PostView.as_view()),
    path('/<int:post_id>', PostDetailView.as_view()),
    path('/<int:post_id>/like', PostLikeView.as_view()),
    path('/<int:post_id>/restore', PostRestoreView.as_view()),
]