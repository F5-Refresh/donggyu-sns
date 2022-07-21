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
from core.utils.get_obj_n_check_err import GetPostDetail, GetUserPostDetail


class PostView(APIView):
    
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
        user = request.user
        
        search   = request.GET.get('search', None)
        hashtags = request.GET.get('hashtags', None)
        sort     = request.GET.get('sort', 'up_to_date')
        status   = request.GET.get('status', 'deleted')
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 10))
        
        sort_set = {
            'up_to_date' : '-created_at',
            'out_of_date': 'created_at',
            'likes'      : '-likes',
            'unlikes'    : 'likes',
            'high_views' : '-views',
            'low_views'  : 'views'
        }
        
        q = Q()
        
        if search:
            q |= Q(title__icontains = search)
            q |= Q(content__icontains = search)
            q |= Q(tags__name__icontains = search)
            
        if hashtags: 
            tags = hashtags.split(',')
            
            """
            TODO
            """
            q &= Q(tags__name__in=tags)

            """
            1)
              q &= Q(tags__name__iexact=tags)
            2)
              for tag in tags:
                  q.add(Q(tags__name__icontains=tag), q.AND)
            """
            
        posts = Post.objects\
                    .annotate(likes=Count('like'))\
                    .select_related('users')\
                    .prefetch_related('tags')\
                    .filter(q)\
                    .exclude(status__iexact=status)\
                    .order_by(sort_set[sort])[offset:offset+limit]
                   
        serializer = PostListSerializer(posts, many=True, context={'user': user})
        return Response(serializer.data, status=200)
    
    @swagger_auto_schema(request_body=PostCreateSerializer, responses={201: PostCreateSerializer})        
    def post(self, request):
        user = request.user
        
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(users=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
  
  
class PostDetailView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    post_id = openapi.Parameter('post_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @query_debugger
    @swagger_auto_schema(responses={200: PostDetailSerializer}, manual_parameters=[post_id])
    def get(self, request, post_id):
        user = request.user
        
        post, err = GetPostDetail.get_post_n_check_error(post_id)
        if err:
            return Response({'detail': err}, status=400)
    
        serializer = PostDetailSerializer(post, context={'user': user})
        return Response(serializer.data, status=200)        
    
    @swagger_auto_schema(
        request_body=PostUpdateSerializer, responses={200: PostUpdateSerializer},\
        manual_parameters=[post_id]
    )
    def patch(self, request, post_id):
        user = request.user
        
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
        user = request.user
        
        post, err = GetUserPostDetail.get_post_n_check_error(post_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if post.status == 'deleted':
            return Response({'detail': f'게시글 {post_id}(id)는 이미 삭제된 상태입니다.'}, status=400)
        
        post.status = 'deleted'
        post.save()
        return Response({'detail': f'게시글 {post_id}(id)가 삭제되었습니다.'}, status=200)


class PostRestoreView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    post_id = openapi.Parameter('post_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(responses={200: '게시글이 복구되었습니다.'}, manual_parameters=[post_id])
    def patch(self, request, post_id):
        user = request.user
        
        post, err = GetUserPostDetail.get_post_n_check_error(post_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if post.status == 'in_posting':
            return Response({'detail': f'게시글 {post_id}(id)는 이미 게시중입니다.'}, status=400)

        post.status = 'in_posting'
        post.save()
        return Response({'detail': f'게시글 {post_id}(id)가 복구되었습니다.'}, status=200)
    
    
class PostLikeView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    post_id = openapi.Parameter('post_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(responses={200: '게시물의 "좋아요"를 눌렀습니다/취소했습니다.'}, manual_parameters=[post_id])
    def post(self, request, post_id):
        user = request.user

        try:
            post = Post.objects\
                       .get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': f'게시물 {post_id}(id)는 존재하지 않습니다.'}, status=400)
        
        like, is_created = Like.objects\
                               .get_or_create(users=user, posts=post)
        if not is_created:
            like.delete()
            return Response({'detail': f'게시물 {post_id}(id)의 "좋아요"를 취소했습니다.'}, status=200)
        
        return Response({'detail': f'게시물 {post_id}(id)의 "좋아요"를 눌렀습니다.'}, status=200)     