from django.db.models import Q, Count

from drf_yasg         import openapi
from drf_yasg.utils   import swagger_auto_schema

from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from posts.models         import Post
from posts.serializers    import PostCreateSerializer, PostListSerializer, PostDetailSerializer
from core.utils.decorator import query_debugger


class PostListView(APIView):
    
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
            
        if hashtags: # TODO
            tags = hashtags.split(',')
            # q &= Q(tags__name__iexact=tags)
            # q &= Q(tags__name__in=tags)
            for tag in tags:
                q.add(Q(tags__name__icontains=tag), q.AND)
            
        posts = Post.objects\
                    .annotate(likes=Count('like'))\
                    .select_related('users')\
                    .prefetch_related('tags')\
                    .filter(q)\
                    .exclude(status__iexact=status)\
                    .order_by(sort_set[sort])[offset:offset+limit]
                   
        serializer = PostListSerializer(posts, many=True, context={'user': user})
        return Response(serializer.data, status=200)
  
  
class PostDetailView(APIView):
    
    permission_classes = [AllowAny]
    
    def get(self, request, post_id):
        pass  


class PostCreateView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=PostCreateSerializer, responses={201: PostCreateSerializer})        
    def post(self, request):
        user = request.user
        
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(users=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PostUpdateDeleteView(APIView):
    
    permission_classes = [IsAuthenticated]

    def pathch(self, request, post_id):
        pass
    
    def delete(self, request, post_id):
        pass


class PostRestoreView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, post_id):
        pass