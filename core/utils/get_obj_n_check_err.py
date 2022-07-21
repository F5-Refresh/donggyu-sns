from typing           import Tuple, Any
from django.db.models import Count

from posts.models import Post
from users.models import User


class GetPostDetail:
    """
    Assignee: 김동규
    
    param: post_id
    return: obj, err
    detail:
      - 게시물 id를 통해 게시물 객체(정보)의 존재여부 확인
      - 게시물의 좋아요 개수도 함께 확인
    """
    
    def get_post_n_check_error(post_id: int) -> Tuple[Any, str]:
        try:
            post = Post.objects\
                       .annotate(likes=Count('like'))\
                       .select_related('users')\
                       .prefetch_related('tags')\
                       .get(id=post_id)
        except Post.DoesNotExist:
            return None, f'게시물 {post_id}(id)는 존재하지 않습니다.'
        
        return post, None
    

class GetUserPostDetail:
    """
    Assignee: 김동규
    
    param: post_id, user
    return: obj, err
    detail:
      - 게시물 id를 통해 게시물 객체(정보)의 존재여부 확인
      - 게시물 객체의 유저정보와 API를 호출한 유저의 정보를 대조
    """
    
    def get_post_n_check_error(post_id: int, user: User) -> Tuple[Any, str]:
        try:
            post = Post.objects\
                       .select_related('users')\
                       .get(id=post_id)
        except Post.DoesNotExist:
            return None, f'게시물 {post_id}(id)는 존재하지 않습니다.'
        
        if not user.nickname == post.users.nickname:
            return None, '다른 유저의 게시물입니다.'
        
        return post, None