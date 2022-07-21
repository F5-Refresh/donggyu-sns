from typing           import Tuple, Any
from django.db.models import Count

from posts.models import Post
from users.models import User


class GetPostDetail:
    
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