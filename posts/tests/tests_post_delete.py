import json

from rest_framework.test import APITestCase, APIClient

from users.models import User
from posts.models import Post, Tag


class PostDeleteTest(APITestCase):
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
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) post obj
            - 게시글 존재여부 확인(존재하지 않는 게시글는 삭제할 수 없음)
            - 게시글 유저정보 확인(다른 유저의 게시글는 삭제할 수 없음)
            - 게시글 상태정보 확인(이미 삭제된 게시글는 다시 삭제할 수 없음)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/게시글/태그 정보)
    """
    
    def setUp(self):
        self.f_user = User.objects\
                          .create_user(
                              email    = 'userTest@example.com',
                              nickname = 'userTest',
                              password = 'Testpassw0rd!'
                          )

        self.s_user = User.objects\
                          .create_user(
                              email    = 'testUser@example.com',
                              nickname = 'testUser',
                              password = 'Testpassw3rd!'
                          )
                        
        self.client = APIClient()
        self.client.force_authenticate(user=self.f_user)
        
        self.f_tag = Tag.objects\
                        .create(
                            id   = 1,
                            name = '#잠실'
                        )
                       
        self.s_tag = Tag.objects\
                        .create(
                            id   = 2,
                            name = '#석촌호수'
                        )

        self.t_tag = Tag.objects\
                        .create(
                            id   = 3,
                            name = '#스타벅스'
                        )
                        
        self.f_post = Post.objects\
                          .create(
                              id      = 1,
                              users   = self.f_user,
                              title   = 'testTitle1',
                              content = 'testContent1'
                          )
                         
        self.f_post.tags.add(self.f_tag)
        self.f_post.tags.add(self.s_tag)
        
        self.s_post = Post.objects\
                          .create(
                              id      = 2,
                              users   = self.s_user,
                              title   = 'testTitle2',
                              content = 'testContent2'
                          )
                         
        self.s_post.tags.add(self.s_tag)
        self.s_post.tags.add(self.t_tag)
        
        self.t_post = Post.objects\
                          .create(
                              id      = 3,
                              users   = self.f_user,
                              title   = 'testTitle3',
                              content = 'testContent3',
                              status  = 'deleted'
                          )
        
        self.t_post.tags.add(self.f_tag)
        self.t_post.tags.add(self.s_tag)
        self.t_post.tags.add(self.t_tag)
    
    """
    테스트 데이터 리셋
    """  
        
    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()
        Tag.objects.all().delete()
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_delete_post(self):
        response = self.client\
                       .delete('/api/posts/1', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'detail': '게시글 1(id)가 삭제되었습니다.'
            }
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_delete_post_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        response = self.client\
                       .delete('/api/posts/1', content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
        
    def test_fail_delete_post_due_to_not_existed_post(self):
        response = self.client\
                       .delete('/api/posts/10', content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '게시글 10(id)는 존재하지 않습니다.'
            }
        )
        
    def test_fail_delete_post_due_to_not_own_post(self):
        response = self.client\
                       .delete('/api/posts/2', content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 게시글입니다.'
            }
        )
        
    def test_fail_delete_post_due_to_already_deleted_post(self):
        response = self.client\
                       .delete('/api/posts/3', content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '게시글 3(id)는 이미 삭제된 상태입니다.'
            }
        )