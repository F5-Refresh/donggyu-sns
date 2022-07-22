from django.db                  import transaction

from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Post, Tag, AccessIp
from users.models import Like


class TagSerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail: (해시)태그 데이터 시리얼라이저[Many-To-Many]
    model: Tag
    """
    
    class Meta:
        model  = Tag
        fields = ['id', 'name']
        extra_kwargs = {
            'id': {'read_only': True}
        }
        

class PostListSerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail: 게시물 리스트 조회 시리얼라이저[GET] 
    model: Post
    """
    
    likes       = serializers.SerializerMethodField()
    like_status = serializers.SerializerMethodField()
    nickname    = serializers.SerializerMethodField()
    created_at  = serializers.SerializerMethodField()
    tags        = TagSerializer(many=True)
    
    def get_likes(self, obj: Post) -> int:
        return obj.like_set.count()
    
    def get_like_status(self, obj: Post) -> bool:
        user = self.context.get('user')
        post = obj
        return Like.objects.filter(users=user, posts=post).exists()
    
    def get_nickname(self, obj: Post) -> str:
        return obj.users.nickname
        
    def get_created_at(self, obj: Post) -> str:
        return (obj.created_at).strftime('%Y-%m-%d %H:%M')
            
    class Meta:
        model  = Post
        fields = [
            'id', 'title', 'nickname', 'content', 'tags', 'created_at',\
            'likes', 'views', 'like_status', 'status'
        ]
        extra_kwargs = {
            'id': {'read_only': True}
        }
        
             
class PostCreateSerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail: 게시물 생성 시리얼라이저[POST] 
    model: Post
    """
    
    tags       = TagSerializer(many=True)
    nickname   = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    
    def get_nickname(self, obj: Post) -> str:
        return obj.users.nickname
    
    def get_created_at(self, obj: Post) -> str:
        return (obj.created_at).strftime('%Y-%m-%d %H:%M')
    
    """
    게시물/해시태그 생성
      - 하나의 게시물을 생성할 때, 여러 개의 해시태그를 함께 생성함
    """
    @transaction.atomic()
    def create(self, validated_data):
        hashtags = validated_data.pop('tags', None)
        
        post = Post.objects\
                   .create(**validated_data)
        
        if not hashtags:
            raise serializers.ValidationError('detail: 해시태그는 필수 입력값입니다.')
        for hashtag in hashtags:
            tag, _ = Tag.objects\
                        .get_or_create(name=hashtag['name'])

            post.tags.add(tag)
            
        return post
    
    class Meta:
        model  = Post
        fields = [
            'id', 'title', 'nickname', 'content', 'tags', 'created_at',\
            'views', 'status'
        ]
        extra_kwargs = {
            'id': {'read_only': True}
        }
        

class PostDetailSerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail: 게시물 상세 조회 시리얼라이저[GET] 
    model: Post
    """
    
    likes       = serializers.SerializerMethodField()
    like_status = serializers.SerializerMethodField()
    nickname    = serializers.SerializerMethodField()
    created_at  = serializers.SerializerMethodField()
    views       = serializers.SerializerMethodField()
    tags        = TagSerializer(many=True)
    
    def get_likes(self, obj: Post) -> int:
        return obj.likes
    
    def get_like_status(self, obj: Post) -> bool:
        user = self.context.get('user')
        post = obj
        return Like.objects.filter(users=user, posts=post).exists()
    
    def get_nickname(self, obj: Post) -> str:
        return obj.users.nickname
        
    def get_created_at(self, obj: Post) -> str:
        return (obj.created_at).strftime('%Y-%m-%d %H:%M')
    
    """
    조회수 증가:
      - 조회수가 ip당 1회만 증가하도록 제한
    """
    @transaction.atomic()
    def get_views(self, obj: Post) -> int:
        ip   = self.context.get('ip')
        post = obj
        
        if not AccessIp.objects.filter(ip=ip, posts=post).exists():
            obj.views += 1
            obj.save()
            
            AccessIp.objects\
                    .create(ip=ip, posts=post)
                    
            return obj.views
        return obj.views

    class Meta:
        model  = Post
        fields = [
            'id', 'title', 'nickname', 'content', 'tags', 'created_at',\
            'views', 'status', 'likes', 'like_status'
        ]
        extra_kwargs = {
            'id': {'read_only': True}
        }
        
        
class PostUpdateSerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail: 게시물 수정 시리얼라이저[PATCH] 
    model: Post
    """
    
    nickname    = serializers.SerializerMethodField()
    created_at  = serializers.SerializerMethodField()
    tags        = TagSerializer(many=True)
    
    def get_nickname(self, obj: Post) -> str:
        return obj.users.nickname
        
    def get_created_at(self, obj: Post) -> str:
        return (obj.created_at).strftime('%Y-%m-%d %H:%M')
    
    """
    게시물/해시태그 수정
      - 하나의 게시물을 수정할 때, 여러 개의 해시태그를 함께 수정함
    """
    @transaction.atomic()
    def update(self, instance: Post, validated_data):
        instance.tags.clear()
        
        instance.title   = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        
        hashtags = validated_data.pop('tags', None)
        
        if not hashtags:
            raise serializers.ValidationError('detail: 해시태그는 필수 입력값입니다.')
        for hashtag in hashtags:
            tag, _ = Tag.objects\
                        .get_or_create(name=hashtag['name'])
            
            instance.tags.add(tag)
            
        instance.save()
        return instance
           
    class Meta:
        model  = Post
        fields = [
            'id', 'title', 'nickname', 'content', 'tags', 'created_at',\
            'views', 'status'
        ]
        extra_kwargs = {
            'id': {'read_only': True}
        }