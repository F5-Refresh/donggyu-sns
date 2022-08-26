import json

from rest_framework.test import APITestCase, APIClient

from datetime     import datetime
from users.models import User


class PostCreateTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(4개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) request body
            - 필수 파라미터 확인: title/content/tags
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저 정보)
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects\
                       .create_user(
                           email    = 'userTest@example.com',
                           nickname = 'userTest',
                           password = 'Testpassw0rd!'
                       )
                       
        cls.f_client = APIClient()
        cls.f_client.force_authenticate(user=cls.user)

    """
    성공 케이스 테스트코드
    """
    
    def test_success_create_post(self):
        data = {
            'title'  : 'testPost',
            'content': 'testContent',
            'tags'   : [
                {
                    'name': '#서울'
                },
                {
                    'name': '#잠실'
                },
                {
                    'name': '#석촌호수'
                },
                {
                    'name': '#동호'
                },
                {
                    'name': '#스타벅스'
                }
            ],
            'views'  : 0,
            'status' : 'in_posting'
        }
        
        response = self.f_client\
                       .post('/api/posts', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'id'      : 1,
                'title'   : 'testPost',
                'nickname': 'userTest',
                'content' : 'testContent',
                'tags'    : [
                    {
                        'id'  : 1,
                        'name': '#서울'
                    },
                    {
                        'id'  : 2,
                        'name': '#잠실'
                    },
                    {
                        'id'  : 3,
                        'name': '#석촌호수'
                    },
                    {
                        'id'  : 4,
                        'name': '#동호'
                    },
                    {
                        'id'  : 5,
                        'name': '#스타벅스'
                    }
                ],
                'created_at': (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                'views'     : 0,
                'status'    : 'in_posting'
            }
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_create_post_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        data = {
            'title'  : 'testPost',
            'content': 'testContent',
            'tags'   : [
                {
                    'name': '#서울'
                },
                {
                    'name': '#잠실'
                },
                {
                    'name': '#석촌호수'
                },
                {
                    'name': '#동호'
                },
                {
                    'name': '#스타벅스'
                }
            ],
            'views'  : 0,
            'status' : 'in_posting'
        }
        
        response = self.client\
                       .post('/api/posts', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
        
    def test_fail_create_post_due_to_title_required(self):
        data = {
            'content': 'testContent',
            'tags'   : [
                {
                    'name': '#서울'
                },
                {
                    'name': '#잠실'
                },
                {
                    'name': '#석촌호수'
                },
                {
                    'name': '#동호'
                },
                {
                    'name': '#스타벅스'
                }
            ],
            'views'  : 0,
            'status' : 'in_posting'
        }
        
        response = self.f_client\
                       .post('/api/posts', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'title': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_create_post_due_to_content_required(self):
        data = {
            'title': 'testPost',
            'tags' : [
                {
                    'name': '#서울'
                },
                {
                    'name': '#잠실'
                },
                {
                    'name': '#석촌호수'
                },
                {
                    'name': '#동호'
                },
                {
                    'name': '#스타벅스'
                }
            ],
            'views'  : 0,
            'status' : 'in_posting'
        }
        
        response = self.f_client\
                       .post('/api/posts', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'content': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_create_post_due_to_tags_required(self):
        data = {
            'title'  : 'testPost',
            'content': 'testContent',
            'views'  : 0,
            'status' : 'in_posting'
        }
        
        response = self.f_client\
                       .post('/api/posts', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'tags': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )