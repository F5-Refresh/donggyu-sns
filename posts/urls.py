from django.urls import path

from posts.views import PostListView, PostDetailView, PostCreateView,\
                        PostUpdateDeleteView, PostRestoreView


"""
게시물 url patterns
"""
urlpatterns = [
    path('', PostCreateView.as_view()),
    path('/list', PostListView.as_view()),
    path('/detail/<int:post_id>', PostDetailView.as_view()),
    path('/<int:post_id>', PostUpdateDeleteView.as_view()),
    path('/<int:post_id>/restore', PostRestoreView.as_view()),
]