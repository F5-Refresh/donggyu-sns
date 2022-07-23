from django.db.models import Q, Count

from drf_yasg         import openapi
from drf_yasg.utils   import swagger_auto_schema

from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from posts.models      import Post
from posts.serializers import PostCreateSerializer, PostListSerializer, PostDetailSerializer, PostUpdateSerializer

from users.models      import Like

from core.utils.decorator           import query_debugger
from core.utils.get_obj_n_check_err import GetPostDetail, GetUserPostDetail, GetClientIp


class PostView(APIView):
    """
    Assignee: 김동규
    
    query string: sort, hashtags, search, status, offset, limit
    return: json
    detail:
      - 인증/인가에 통과한 유저는 본인의 게시글 리스트 정보를 호출할 수 있습니다.(GET: 게시글 리스트 조회 기능)
        > 부가기능:
          * 게시글 검색기능
          * 해시태그 검색기능
          * 정렬 기능(생성일자, 좋아요, 조회수를 기준으로 정렬)
          * 게시글 필터링 기능(사용중인 게시글/삭제된 게시글)
          * 페이지네이션 기능(원하는 크기의 데이터 개수를 호출)
      - 인증/인가에 통과한 유저가 게시글을 생성할 수 있습니다.(POST: 게시글 생성 기능)
    """
    
    permission_classes = [IsAuthenticated]
    
    sort     = openapi.Parameter('sort', openapi.IN_QUERY, required=False, pattern='?sort=', type=openapi.TYPE_STRING)
    hashtags = openapi.Parameter('hashtags', openapi.IN_QUERY, required=False, pattern='?hashtags=', type=openapi.TYPE_STRING)
    search   = openapi.Parameter('search', openapi.IN_QUERY, required=False, pattern='?search=', type=openapi.TYPE_STRING)
    status   = openapi.Parameter('status', openapi.IN_QUERY, required=False, pattern='?status=', type=openapi.TYPE_STRING)
    offset   = openapi.Parameter('offset', openapi.IN_QUERY, required=False, pattern='?offset=', type=openapi.TYPE_STRING)
    limit    = openapi.Parameter('limit', openapi.IN_QUERY, required=False, pattern='?limit=', type=openapi.TYPE_STRING)
    
    @query_debugger
    @swagger_auto_schema(responses={200: PostListSerializer}, manual_parameters=[sort, hashtags, search, status, offset, limit])
    def get(self, request):
        """
        GET: 게시글 조회(리스트) 기능
        """
        user = request.user
        
        search   = request.GET.get('search', None)
        hashtags = request.GET.get('hashtags', None)
        sort     = request.GET.get('sort', 'up_to_date')
        status   = request.GET.get('status', 'deleted')
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 10))
        
        """
        정렬 기준
        """ 
        sort_set = {
            'up_to_date' : '-created_at',
            'out_of_date': 'created_at',
            'likes'      : '-likes',
            'unlikes'    : 'likes',
            'high_views' : '-views',
            'low_views'  : 'views'
        }
        
        q = Q()
        
        """
        검색 기능
        """
        if search:
            q |= Q(title__icontains = search)
            q |= Q(content__icontains = search)
            q |= Q(tags__name__icontains = search)
        
        """
        해시태그 검색기능
        """    
        if hashtags: 
            tags = hashtags.split(',')
        
            q &= Q(tags__name__in=tags)
        
        """
        TODO:
          * resolve this issue >> Post.objects.filter(Q(tags__name__in=tags)) without annotate()
        """    
        posts = Post.objects\
                    .annotate(likes=Count('like'))\
                    .select_related('users')\
                    .prefetch_related('tags', 'like_set')\
                    .filter(q)\
                    .exclude(status__iexact=status)\
                    .order_by(sort_set[sort])[offset:offset+limit]
                   
        serializer = PostListSerializer(posts, many=True, context={'user': user})
        return Response(serializer.data, status=200)
    
    @swagger_auto_schema(request_body=PostCreateSerializer, responses={201: PostCreateSerializer})        
    def post(self, request):
        """
        POST: 게시글 생성 기능
        """
        user = request.user
        
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(users=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
  
  
class PostDetailView(APIView):
    """
    Assignee: 김동규
    
    query param: post_id
    return: json
    detail:
      - 인증/인가에 통과한 유저는 모든 게시글을 조회할 수 있습니다.(GET: 게시글 상세 조회 기능)
      - 인증/인가에 통과한 유저는 본인의 게시글을 수정할 수 있습니다.(PATCH: 게시글 수정 기능)
      - 인증/인가에 통과한 유저는 본인의 게시글을 삭제할 수 있습니다.(DELETE: 게시글 삭제 기능)
    """
    
    permission_classes = [IsAuthenticated]
    
    post_id = openapi.Parameter('post_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @query_debugger
    @swagger_auto_schema(responses={200: PostDetailSerializer}, manual_parameters=[post_id])
    def get(self, request, post_id):
        """
        GET: 게시글 조회(상세) 기능[조회수 증가]
        """
        user = request.user
        
        """
        요청 클라이언트 ip정보 추출
        """
        ip = GetClientIp.get_client_ip(request)
        
        """
        게시글 객체 확인
        """
        post, err = GetPostDetail.get_post_n_check_error(post_id)
        if err:
            return Response({'detail': err}, status=400)
    
        serializer = PostDetailSerializer(post, context={'user': user, 'ip': ip})
        return Response(serializer.data, status=200)        
    
    @swagger_auto_schema(
        request_body=PostUpdateSerializer, responses={200: PostUpdateSerializer},\
        manual_parameters=[post_id]
    )
    def patch(self, request, post_id):
        """
        PATCH: 게시글 수정 기능(게시글 제목/내용/해시태그 수정)
        """
        user = request.user
        
        """
        게시글 객체/유저정보 확인
        """
        post, err = GetUserPostDetail.get_post_n_check_error(post_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        serializer = PostUpdateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    @swagger_auto_schema(responses={200: '게시글이 삭제되었습니다.'}, manual_parameters=[post_id])
    def delete(self, request, post_id):
        """
        DELETE: 게시글 삭제 기능
        """
        user = request.user
        
        """
        게시글 객체/유저정보 확인
        """
        post, err = GetUserPostDetail.get_post_n_check_error(post_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if post.status == 'deleted':
            return Response({'detail': f'게시글 {post_id}(id)는 이미 삭제된 상태입니다.'}, status=400)
        
        post.status = 'deleted'
        post.save()
        return Response({'detail': f'게시글 {post_id}(id)가 삭제되었습니다.'}, status=200)


class PostRestoreView(APIView):
    """
    Assignee: 김동규
    
    query param: post_id
    return: json
    detail: 인증/인가에 통과한 유저는 본인의 게시글을 복구할 수 있습니다.(PATCH: 게시글 복구 기능)
    """
    
    permission_classes = [IsAuthenticated]
    
    post_id = openapi.Parameter('post_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(responses={200: '게시글이 복구되었습니다.'}, manual_parameters=[post_id])
    def patch(self, request, post_id):
        """
        PATCH: 게시글 복구 기능
        """
        user = request.user
        
        """
        게시글 객체/유저정보 확인
        """
        post, err = GetUserPostDetail.get_post_n_check_error(post_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if post.status == 'in_posting':
            return Response({'detail': f'게시글 {post_id}(id)는 이미 게시중입니다.'}, status=400)

        post.status = 'in_posting'
        post.save()
        return Response({'detail': f'게시글 {post_id}(id)가 복구되었습니다.'}, status=200)
    
    
class PostLikeView(APIView):
    """
    Assignee: 김동규
    
    query param: post_id
    return: json
    detail: 인증/인가에 통과한 유저는 모든 게시글에 "좋아요"를 누르거나 취소할 수 있습니다.(POST: 좋아요 생성/취소 기능)
    """
    
    permission_classes = [IsAuthenticated]
    
    post_id = openapi.Parameter('post_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(responses={200: '게시글의 "좋아요"를 눌렀습니다/취소했습니다.'}, manual_parameters=[post_id])
    def post(self, request, post_id):
        """
        POST: 게시글 좋아요 생성/취소 기능
        """
        user = request.user
        
        """
        게시글 객체 확인
        """
        try:
            post = Post.objects\
                       .get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': f'게시글 {post_id}(id)는 존재하지 않습니다.'}, status=400)
        
        """
        좋아요 생성/취소 
        """
        like, is_created = Like.objects\
                               .get_or_create(users=user, posts=post)
        if not is_created:
            like.delete()
            return Response({'detail': f'게시글 {post_id}(id)의 "좋아요"를 취소했습니다.'}, status=200)
        
        return Response({'detail': f'게시글 {post_id}(id)의 "좋아요"를 눌렀습니다.'}, status=200)     