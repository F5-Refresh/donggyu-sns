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
      - 게시글 id를 통해 게시글 객체(정보)의 존재여부 확인
      - 게시글의 좋아요 개수도 함께 확인
    """
    
    def get_post_n_check_error(post_id: int) -> Tuple[Any, str]:
        try:
            post = Post.objects\
                       .annotate(likes=Count('like'))\
                       .select_related('users')\
                       .get(id=post_id)
        except Post.DoesNotExist:
            return None, f'게시글 {post_id}(id)는 존재하지 않습니다.'
        
        return post, None
    

class GetUserPostDetail:
    """
    Assignee: 김동규
    
    param: post_id, user
    return: obj, err
    detail:
      - 게시글 id를 통해 게시글 객체(정보)의 존재여부 확인
      - 게시글 객체의 유저정보와 API를 호출한 유저의 정보를 대조
    """
    
    def get_post_n_check_error(post_id: int, user: User) -> Tuple[Any, str]:
        try:
            post = Post.objects\
                       .select_related('users')\
                       .get(id=post_id)
        except Post.DoesNotExist:
            return None, f'게시글 {post_id}(id)는 존재하지 않습니다.'
        
        if not user.nickname == post.users.nickname:
            return None, '다른 유저의 게시글입니다.'
        
        return post, None
    
    
class GetClientIp:
    """
    Assignee: 김동규
    
    param: request
    return: obj
    detail:
      - request obj에서 요청 클라이언트의 IP정보를 추출함
    """
    
    def get_client_ip(request: object) -> object:
        """
        HTTP_X_FORWARDED_FOR(XFF):
          - XFF는 HTTP Header 중 하나로 HTTP Server에 요청한 Client의 IP를 식별하기 위한 표준임
          - HTTP_X_FORWARDED_FOR: client, proxy1, proxy2 etc..
            * client: 실제 클라이언트의 IP
            * proxy0: Proxy 서버의 IP
            
        REMOTE_ADDR:
          - TCP/IP 접속 그 자체에서 생성되는 값으로, 접속자의 IP 주소 값을 가지고 있음
        """
        
        HTTP_X_FORWARDED_FOR = request.META.get('HTTP_X_FORWARDED_FOR')

        if HTTP_X_FORWARDED_FOR:
            IP = HTTP_X_FORWARDED_FOR.split(',')[0]
        
        IP = request.META.get('REMOTE_ADDR')
        return IP