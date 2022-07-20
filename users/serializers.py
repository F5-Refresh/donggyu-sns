import re

from django.contrib.auth.hashers          import check_password

from rest_framework                       import serializers
from rest_framework.serializers           import ModelSerializer, Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserSignUpSerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail:
      - 유저 데이터 시리얼라이저[POST 기능 유효성 검사]
      - 패스워드 정규식 표현을 기준으로 패스워드 형식 유효성 검사
      - 유저정보를 DB에 저장할 때, 패스워드 해싱 후 저장
    model: User
    """
    
    def create(self, validated_data):
        password = validated_data.get('password')
        
        """
        패스워드 정규식표현(길이 8~20 자리, 최소 1개 이상의 소문자, 대문자, 숫자, (숫자키)특수문자로 구성)
        """
        password_regex = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,20}$'
        
        if not re.match(password_regex, password):
            raise serializers.ValidationError({'detail': ['올바른 비밀번호를 입력하세요.']})
        
        """
        유저정보 DB에 저장
        """
        user = User.objects.create_user(**validated_data)
        return user
        
    class Meta:
        model        = User
        fields       = ['email', 'nickname', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
        
class UserSignInSerializer(TokenObtainPairSerializer):
    """
    Assignee: 김동규
    
    detail:
      - 유저 데이터 시리얼라이저[POST 기능 유효성 검사]
      - 이메일 형식에 맞는지 유효성 검사
      - 패스워드가 DB에 있는 유저 패스워드와 일치하는지 유효성 검사
      - 모든 유효성 검사에 통과하면 액세스 토큰과 리프레시 토큰을 발급
    model: User
    """
    
    email    = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, write_only=True, max_length=100)
    
    def validate(self, data):
        email    = data.get('email')
        password = data.get('password')
        
        """
        입력받은 이메일 정보에 해당하는 유저 객체를 불러옵니다.
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('detail: 올바른 유저정보를 입력하세요.')
        
        """
        입력받은 패스워드 정보가 해당 유저의 패스워드와 일치하는지 확인합니다.
        """
        if not check_password(password, user.password):
            raise serializers.ValidationError('detail: 올바른 유저정보를 입력하세요.')
        
        """
        액세스 토큰과 리프레시 토큰을 발급합니다.
        """
        token         = super().get_token(user)
        refresh_token = str(token)
        access_token  = str(token.access_token)
        
        data = {
            'refresh' : refresh_token,
            'access'  : access_token
        }
        return data
        
    class Meta:
        model  = User
        fields = ['email', 'password']
        

class UserSignInSchema(Serializer):
    """
    Assignee: 김동규
    
    detail: 유저토큰 스키마 시리얼라이저[only used for swagger]
    """
    
    refresh = serializers.CharField(max_length=255)
    access  = serializers.CharField(max_length=255)