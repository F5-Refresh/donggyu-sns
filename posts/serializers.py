from django.db                  import transaction

from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Post, Tag
from users.models import Like


class TagSerializer(ModelSerializer):
    
    class Meta:
        model  = Tag
        fields = ['id', 'name']
        extra_kwargs = {
            'id': {'read_only': True}
        }
        

class PostListSerializer(ModelSerializer):
    likes       = serializers.SerializerMethodField()
    like_status = serializers.SerializerMethodField()
    nickname    = serializers.SerializerMethodField()
    created_at  = serializers.SerializerMethodField()
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
    tags       = TagSerializer(many=True)
    nickname   = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    
    def get_nickname(self, obj: Post) -> str:
        return obj.users.nickname
    
    def get_created_at(self, obj: Post) -> str:
        return (obj.created_at).strftime('%Y-%m-%d %H:%M')
    
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
    pass