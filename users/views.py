from rest_framework.views            import APIView
from rest_framework.response         import Response
from rest_framework.permissions      import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken, RefreshToken

from drf_yasg       import openapi
from drf_yasg.utils import swagger_auto_schema

from users.serializers import UserSignUpSerializer, UserSignInSerializer, UserSignInSchema


class UserSignUpView(APIView):
    """
    Assignee: 김동규
    
    request body
      - 필수: email, nickname, password
      - 선택: phone number, profile image
    return: json
    detail: 유저 회원가입 기능입니다.
    """
    
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=UserSignUpSerializer, responses={201: UserSignUpSerializer})
    def post(self, request):
        """
        POST: 유저 회원가입 기능
        """
        serializer = UserSignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
class UserSignInView(APIView):
    """
    Assignee: 김동규
    
    request body: email, password
    return: json
    detail: 유저 로그인 기능입니다.
    """
    
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=UserSignInSerializer, responses={200: UserSignInSchema})
    def post(self, request):
        """
        POST: 유저 로그인 기능
        """
        serializer = UserSignInSerializer(data=request.data)
        
        if serializer.is_valid():
            token = serializer.validated_data
            return Response(token, status=200)
        return Response(serializer.errors, status=400)
    

class UserSignOutView(APIView):
    """
    Assignee: 김동규
    
    request body: refresh token
    return: json
    detail: 유저 로그아웃 기능입니다.
    """
    
    permission_classes = [IsAuthenticated]
    
    post_params = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'refesh_token': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    )
    @swagger_auto_schema(request_body=post_params, responses={200: '유저가 로그아웃 되었습니다.'})
    def post(self, request):
        """
        POST: 유저 로그아웃 기능
        """
        user = request.user
        
        """
        해당 유저의 리프레시 토큰 정보를 가져옵니다.
        """
        try:
            refresh = RefreshToken(request.data['refesh_token'])
        except:
            return Response({'detail': '유효하지 않거나 만료된 토큰입니다.'}, status=400)
        
        """
        해당 유저의 발급된 모든 리프레시 토큰을 사용 제한합니다.
        """
        for token in OutstandingToken.objects.filter(user_id=refresh['user_id']):
            BlacklistedToken.objects.get_or_create(token=token)
            
        return Response({'message' : f'유저 {user.nickname}이 로그아웃 되었습니다.'}, status=200)