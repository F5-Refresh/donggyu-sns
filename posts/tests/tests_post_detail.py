from datetime import datetime

from rest_framework.test import APITestCase, APIClient

from users.models import User, Like
from posts.models import Post, Tag


class PostDetailTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(2개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) post obj
            - 게시글 존재여부 확인(존재하지 않는 게시글은 상세 조회할 수 없음)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/게시글/태그/좋아요 정보)
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.f_user = User.objects\
                         .create_user(
                             email    = 'userTest@example.com',
                             nickname = 'userTest',
                             password = 'Testpassw0rd!'
                         )
        
        cls.f_client = APIClient()
        cls.f_client.force_authenticate(user=cls.f_user)
        
        cls.f_tag = Tag.objects\
                       .create(
                           id   = 1,
                           name = '#잠실'
                       )
                       
        cls.s_tag = Tag.objects\
                       .create(
                           id   = 2,
                           name = '#석촌호수'
                       )

        cls.t_tag = Tag.objects\
                       .create(
                           id   = 3,
                           name = '#스타벅스'
                       )
        
        cls.f_post = Post.objects\
                         .create(
                             id      = 1,
                             users   = cls.f_user,
                             title   = 'testTitle1',
                             content = 'testContent1',
                         )
                         
        cls.f_post.tags.add(cls.f_tag)
        cls.f_post.tags.add(cls.s_tag)
        cls.f_post.tags.add(cls.t_tag)
        
        Like.objects\
            .create(
                posts = cls.f_post,
                users = cls.f_user
            )
            
    """
    성공 케이스 테스트코드
    """
            
    def test_success_detail_post(self):
        response = self.f_client\
                       .get('/api/posts/1', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'id'      : 1,
                'title'   : 'testTitle1',
                'nickname': 'userTest',
                'content' : 'testContent1',
                'tags'    : [
                    {
                        'id'  : 1,
                        'name': '#잠실'
                    },
                    {
                        'id'  : 2,
                        'name': '#석촌호수'
                    },
                    {
                        'id'  : 3,
                        'name': '#스타벅스'
                    }
                ],
                'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                'likes'      : 1,
                'views'      : 1,
                'like_status': True,
                'status'     : 'in_posting'
            }
        )
        
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_detail_post_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        response = self.client\
                       .get('/api/posts/1', content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
        
    def test_fail_detail_post_due_to_not_existed_post(self):
        response = self.f_client\
                       .get('/api/posts/10', content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '게시글 10(id)는 존재하지 않습니다.'
            }
        )