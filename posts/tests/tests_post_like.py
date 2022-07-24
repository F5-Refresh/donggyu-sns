from rest_framework.test import APITestCase, APIClient

from users.models import User, Like
from posts.models import Post, Tag


class PostLikeTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(2개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(2개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) post obj
            - 게시글 존재여부 확인(존재하지 않는 게시글에 "좋아요" 기능을 사용할 수 없음)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/게시글/태그/좋아요 정보)
    """
    
    def setUp(self):
        self.f_user = User.objects\
                          .create_user(
                              email    = 'userTest@example.com',
                              nickname = 'userTest',
                              password = 'Testpassw0rd!'
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
                              users   = self.f_user,
                              title   = 'testTitle2',
                              content = 'testContent2'
                          )
                         
        self.s_post.tags.add(self.s_tag)
        self.s_post.tags.add(self.t_tag)
        
        Like.objects\
            .create(
                posts = self.s_post,
                users = self.f_user
            )
            
    """
    테스트 데이터 리셋
    """
            
    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()
        Tag.objects.all().delete()
        Like.objects.all().delete()
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_like_post(self):
        response = self.client\
                       .post('/api/posts/1/like', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'detail': '게시글 1(id)의 "좋아요"를 눌렀습니다.'
            }
        )
    
    def test_success_unlike_post(self):
        response = self.client\
                       .post('/api/posts/2/like', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'detail': '게시글 2(id)의 "좋아요"를 취소했습니다.'
            }
        )
    
    """
    실패 케이스 테스트코드
    """
    
    def test_fail_like_post_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        response = self.client\
                       .post('/api/posts/1/like', content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    
    def test_fail_like_post_due_to_not_existed_post(self):
        response = self.client\
                       .post('/api/posts/10/like', content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '게시글 10(id)는 존재하지 않습니다.'
            }
        )