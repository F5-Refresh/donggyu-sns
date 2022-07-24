from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import AllowAny

from drf_yasg.utils    import swagger_auto_schema

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