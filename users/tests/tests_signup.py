import json

from rest_framework.test import APITestCase

from users.models import User


class UserSignUpTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(14개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) email
            - 필수 파라미터 확인
            - 이메일 형식인지 확인
            - 이미 존재하는 이메일인지 확인
        2) nickname
            - 필수 파라미터 확인
            - 이미 존재하는 닉네임인지 확인
        3) password
            - 필수 파라미터 확인
            - 패스워드가 8~20자리인지 확인
            - 패스워드가 최소 1개 이상의 숫자/소문자/대문자/(숫자키)특수문자를 가지는지 확인
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업
    """
    
    @classmethod
    def setUpTestData(cls):
        User.objects\
            .create_user(
                email    = 'userTest@example.com',
                nickname = 'userTest',
                password = 'Testpassw0rd!'
        )
            
    """
    성공 케이스 테스트코드
    """
    
    def test_success_user_signup(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'email'   : 'testUser@example.com',
                'nickname': 'testUser'
            }
        )

    """
    실패 케이스 테스트코드
    """
    
    def test_fail_user_signup_due_to_email_format_validation(self):
        data = {
            'email'   : 'testUserEmail',
            'nickname': 'testUser',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    '유효한 이메일 주소를 입력하십시오.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_email_required(self):
        data = {
            'nickname': 'testUser',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_already_existed_email(self):
        data = {
            'email'   : 'userTest@example.com',
            'nickname': 'testuser',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    'user의 email은/는 이미 존재합니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_already_existed_email_n_nickname(self):
        data = {
            'email'   : 'userTest@example.com',
            'nickname': 'userTest',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    'user의 email은/는 이미 존재합니다.'
                ],
                'nickname': [
                    'user의 nickname은/는 이미 존재합니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_nickname_required(self):
        data = {
            'email'   : 'testUser@example.com',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'nickname': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_already_existed_nickname(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'userTest',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'nickname': [
                    'user의 nickname은/는 이미 존재합니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_gt_20_digit(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'testPassw00000000000000rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_lt_8_digit(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'T3st!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_required(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'password': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_no_small_letters(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'TESTPASSW0RD!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_no_capital_letters(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'testpassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_no_number(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'testPassword!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_no_special_letters(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'testPassw0rd'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_unexpected_special_letters(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'testPassw0rd?'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )