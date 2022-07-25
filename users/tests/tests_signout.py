import json

from rest_framework.test             import APITestCase, APIClient
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken

from users.models import User


class UserSignOutTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(3개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) refresh token
            - 필수 파라미터 확인
            - 유효한 토큰인지 확인
            - 만료된 토큰인지 확인
            - API 요청에 사용한 refresh 토큰과 로그아웃으로 blacklist에 포함된 토큰이 일치하는지 확인
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저 회원가입 정보/로그인 정보)
    """
    
    def setUp(self):
        self.user = User.objects\
                        .create_user(
                            email    = 'userTest@example.com',
                            nickname = 'userTest',
                            password = 'Testpassw0rd!'
                        )
                        
        response = self.client\
                       .post('/api/users/signin',
                             data=json.dumps(
                                 {
                                     'email'   : 'userTest@example.com',
                                     'password': 'Testpassw0rd!'
                                 }
                             ), 
                             content_type='application/json'
                       )                
                        
        self.obj = OutstandingToken.objects\
                                   .get(token=response.json()['refresh'])
                                      
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
    def tearDown(self):
        User.objects.all().delete()
        OutstandingToken.objects.all().delete()
        BlacklistedToken.objects.all().delete()

    """
    성공 케이스 테스트코드
    """
    
    def test_success_user_signout(self):            
        data = {
            'refesh_token': self.obj.token
        }
        
        response = self.client\
                       .post('/api/users/signout', data=json.dumps(data), content_type='application/json')
        
        blacklist_token = BlacklistedToken.objects\
                                          .get(token_id=self.obj.id)
                        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.obj.id, blacklist_token.token_id)
        self.assertEqual(
            response.json(),
            {
                'message': '유저 userTest이 로그아웃 되었습니다.'
            }
        )
    
    """
    실패 케이스 테스트코드
    """
    
    def test_fail_user_signout_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        data = {
            'refesh_token': self.obj.token
        }
        
        response = self.client\
                       .post('/api/users/signout', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    
    def test_fail_user_signout_due_to_refresh_token_required(self):
        data = {
            'refesh_token': ''
        }
        
        response = self.client\
                       .post('/api/users/signout', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '유효하지 않거나 만료된 토큰입니다.'
            }
        )
    
    def test_fail_user_signout_due_to_invalid_refresh_token(self):
        data = {
            'refesh_token': 'fake token'
        }
        
        response = self.client\
                       .post('/api/users/signout', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '유효하지 않거나 만료된 토큰입니다.'
            }
        )