from datetime import datetime

from rest_framework.test import APITestCase, APIClient

from users.models import User, Like
from posts.models import Post, Tag


class PostListTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(12개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(1개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) query string(선택 파라미터)
            - search
            - status
            - hashtags
            - offset/limit
              * in data range: 데이터 범위내(해당 개수의 데이터 반환)
              * out of data range: 데이터 범위밖(0개의 데이터 반환)
            - sort
              * up_to_date: 최신순
              * out_of_date: 오래된순
              * likes: 좋아요 높은순
              * unlikes: 좋아요 낮은순
              * high_views: 조회수 높은순
              * low_views: 조회수 낮은순
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
                       
        cls.s_user = User.objects\
                         .create_user(
                             email    = 'testUser@example.com',
                             nickname = 'testUser',
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
                             views   = 1
                         )
                         
        cls.f_post.tags.add(cls.f_tag)
        cls.f_post.tags.add(cls.s_tag)
        
        cls.s_post = Post.objects\
                         .create(
                             id      = 2,
                             users   = cls.f_user,
                             title   = 'testTitle2',
                             content = 'testContent2',
                             views   = 2
                         )
                         
        cls.s_post.tags.add(cls.s_tag)
        cls.s_post.tags.add(cls.t_tag)
        
        cls.t_post = Post.objects\
                         .create(
                             id      = 3,
                             users   = cls.f_user,
                             title   = 'testTitle3',
                             content = 'testContent3',
                             views   = 3
                         )
                         
        cls.t_post.tags.add(cls.f_tag)
        cls.t_post.tags.add(cls.t_tag)
        
        cls.d_post = Post.objects\
                         .create(
                             id      = 4,
                             users   = cls.f_user,
                             title   = 'testTitle4',
                             content = 'testContent4',
                             status  = 'deleted',
                             views   = 4
                         )
                         
        cls.d_post.tags.add(cls.f_tag)
        cls.d_post.tags.add(cls.s_tag)
        cls.d_post.tags.add(cls.t_tag)
        
        Like.objects\
            .create(
                posts = cls.f_post,
                users = cls.f_user
            )
            
        Like.objects\
            .create(
                posts = cls.f_post,
                users = cls.s_user
            )
            
        Like.objects\
            .create(
                posts = cls.s_post,
                users = cls.f_user
            )
            
    """
    성공 케이스 테스트코드
    """
        
    def test_success_list_post_without_any_condition(self):
        response = self.f_client\
                       .get('/api/posts', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 3,
                    'title'   : 'testTitle3',
                    'nickname': 'userTest',
                    'content' : 'testContent3',
                    'tags'    : [
                        {
                            'id'  : 1,
                            'name': '#잠실'
                        },
                        {
                            'id'  : 3,
                            'name': '#스타벅스'
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 0,
                    'views'      : 3,
                    'like_status': False,
                    'status'     : 'in_posting'
                },
                {
                    'id'      : 2,
                    'title'   : 'testTitle2',
                    'nickname': 'userTest',
                    'content' : 'testContent2',
                    'tags'    : [
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
                    'views'      : 2,
                    'like_status': True,
                    'status'     : 'in_posting'
                },
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
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 2,
                    'views'      : 1,
                    'like_status': True,
                    'status'     : 'in_posting'
                }
            ]
        )    
    
    def test_success_list_post_with_search_filter(self):
        search   = '석촌호수'
        response = self.f_client\
                       .get(f'/api/posts?search={search}', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 2,
                    'title'   : 'testTitle2',
                    'nickname': 'userTest',
                    'content' : 'testContent2',
                    'tags'    : [
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
                    'views'      : 2,
                    'like_status': True,
                    'status'     : 'in_posting'
                },
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
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 2,
                    'views'      : 1,
                    'like_status': True,
                    'status'     : 'in_posting'
                }
            ]
        )    
        
    def test_success_list_post_with_hashtags_filter(self):
        hashtags = '#잠실'
        response = self.f_client\
                       .get(f'/api/posts?hashtags={hashtags}', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 3,
                    'title'   : 'testTitle3',
                    'nickname': 'userTest',
                    'content' : 'testContent3',
                    'tags'    : [
                        {
                            'id'  : 1,
                            'name': '#잠실'
                        },
                        {
                            'id'  : 3,
                            'name': '#스타벅스'
                    }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 0,
                    'views'      : 3,
                    'like_status': False,
                    'status'     : 'in_posting'
                },
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
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 2,
                    'views'      : 1,
                    'like_status': True,
                    'status'     : 'in_posting'
                }
            ]
        )
    
    def test_success_list_post_with_deleted_status_filter(self):
        status = 'in_posting'
        response = self.f_client\
                       .get(f'/api/posts?status={status}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 4,
                    'title'   : 'testTitle4',
                    'nickname': 'userTest',
                    'content' : 'testContent4',
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
                    'likes'      : 0,
                    'views'      : 4,
                    'like_status': False,
                    'status'     : 'deleted'
                }
            ]
        )
    
    def test_success_list_post_with_up_to_date_sorting(self):
        sort     = 'up_to_date'
        response = self.f_client\
                       .get(f'/api/posts?sort={sort}', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 3,
                    'title'   : 'testTitle3',
                    'nickname': 'userTest',
                    'content' : 'testContent3',
                    'tags'    : [
                        {
                            'id'  : 1,
                            'name': '#잠실'
                        },
                        {
                            'id'  : 3,
                            'name': '#스타벅스'
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 0,
                    'views'      : 3,
                    'like_status': False,
                    'status'     : 'in_posting'
                },
                {
                    'id'      : 2,
                    'title'   : 'testTitle2',
                    'nickname': 'userTest',
                    'content' : 'testContent2',
                    'tags'    : [
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
                    'views'      : 2,
                    'like_status': True,
                    'status'     : 'in_posting'
                },
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
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 2,
                    'views'      : 1,
                    'like_status': True,
                    'status'     : 'in_posting'
                }
            ]
        )
    
    def test_success_list_post_with_out_of_date_sorting(self):
        sort     = 'out_of_date'
        response = self.f_client\
                       .get(f'/api/posts?sort={sort}', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
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
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 2,
                    'views'      : 1,
                    'like_status': True,
                    'status'     : 'in_posting'
                },
                {
                    'id'      : 2,
                    'title'   : 'testTitle2',
                    'nickname': 'userTest',
                    'content' : 'testContent2',
                    'tags'    : [
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
                    'views'      : 2,
                    'like_status': True,
                    'status'     : 'in_posting'
                },
                {
                    'id'      : 3,
                    'title'   : 'testTitle3',
                    'nickname': 'userTest',
                    'content' : 'testContent3',
                    'tags'    : [
                        {
                            'id'  : 1,
                            'name': '#잠실'
                        },
                        {
                            'id'  : 3,
                            'name': '#스타벅스'
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 0,
                    'views'      : 3,
                    'like_status': False,
                    'status'     : 'in_posting'
                }
            ]
        )
    
    def test_success_list_post_with_likes_sorting(self):
        sort     = 'likes'
        response = self.f_client\
                       .get(f'/api/posts?sort={sort}', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
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
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 2,
                    'views'      : 1,
                    'like_status': True,
                    'status'     : 'in_posting'
                },
                {
                    'id'      : 2,
                    'title'   : 'testTitle2',
                    'nickname': 'userTest',
                    'content' : 'testContent2',
                    'tags'    : [
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
                    'views'      : 2,
                    'like_status': True,
                    'status'     : 'in_posting'
                },
                {
                    'id'      : 3,
                    'title'   : 'testTitle3',
                    'nickname': 'userTest',
                    'content' : 'testContent3',
                    'tags'    : [
                        {
                            'id'  : 1,
                            'name': '#잠실'
                        },
                        {
                            'id'  : 3,
                            'name': '#스타벅스'
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 0,
                    'views'      : 3,
                    'like_status': False,
                    'status'     : 'in_posting'
                }
            ]
        )
        
    def test_success_list_post_with_unlikes_sorting(self):
        sort     = 'unlikes'
        response = self.f_client\
                       .get(f'/api/posts?sort={sort}', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 3,
                    'title'   : 'testTitle3',
                    'nickname': 'userTest',
                    'content' : 'testContent3',
                    'tags'    : [
                        {
                            'id'  : 1,
                            'name': '#잠실'
                        },
                        {
                            'id'  : 3,
                            'name': '#스타벅스'
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 0,
                    'views'      : 3,
                    'like_status': False,
                    'status'     : 'in_posting'
                },
                {
                    'id'      : 2,
                    'title'   : 'testTitle2',
                    'nickname': 'userTest',
                    'content' : 'testContent2',
                    'tags'    : [
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
                    'views'      : 2,
                    'like_status': True,
                    'status'     : 'in_posting'
                },
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
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 2,
                    'views'      : 1,
                    'like_status': True,
                    'status'     : 'in_posting'
                }
            ]
        )
    
    def test_success_list_post_with_high_views_sorting(self):
        sort     = 'high_views'
        response = self.f_client\
                       .get(f'/api/posts?sort={sort}', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 3,
                    'title'   : 'testTitle3',
                    'nickname': 'userTest',
                    'content' : 'testContent3',
                    'tags'    : [
                        {
                            'id'  : 1,
                            'name': '#잠실'
                        },
                        {
                            'id'  : 3,
                            'name': '#스타벅스'
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 0,
                    'views'      : 3,
                    'like_status': False,
                    'status'     : 'in_posting'
                },
                {
                    'id'      : 2,
                    'title'   : 'testTitle2',
                    'nickname': 'userTest',
                    'content' : 'testContent2',
                    'tags'    : [
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
                    'views'      : 2,
                    'like_status': True,
                    'status'     : 'in_posting'
                },
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
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 2,
                    'views'      : 1,
                    'like_status': True,
                    'status'     : 'in_posting'
                }
            ]
        )
        
    def test_success_list_post_with_low_views_sorting(self):
        sort     = 'low_views'
        response = self.f_client\
                       .get(f'/api/posts?sort={sort}', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
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
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 2,
                    'views'      : 1,
                    'like_status': True,
                    'status'     : 'in_posting'
                },
                {
                    'id'      : 2,
                    'title'   : 'testTitle2',
                    'nickname': 'userTest',
                    'content' : 'testContent2',
                    'tags'    : [
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
                    'views'      : 2,
                    'like_status': True,
                    'status'     : 'in_posting'
                },
                {
                    'id'      : 3,
                    'title'   : 'testTitle3',
                    'nickname': 'userTest',
                    'content' : 'testContent3',
                    'tags'    : [
                        {
                            'id'  : 1,
                            'name': '#잠실'
                        },
                        {
                            'id'  : 3,
                            'name': '#스타벅스'
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 0,
                    'views'      : 3,
                    'like_status': False,
                    'status'     : 'in_posting'
                }
            ]
        )
    
    def test_success_list_post_with_offset_limit_in_data_range(self):
        offset = '0'
        limit  = '2'
        
        response = self.f_client\
                       .get(f'/api/posts?offset={offset}&limit={limit}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 3,
                    'title'   : 'testTitle3',
                    'nickname': 'userTest',
                    'content' : 'testContent3',
                    'tags'    : [
                        {
                            'id'  : 1,
                            'name': '#잠실'
                        },
                        {
                            'id'  : 3,
                            'name': '#스타벅스'
                        }
                    ],
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'likes'      : 0,
                    'views'      : 3,
                    'like_status': False,
                    'status'     : 'in_posting'
                },
                {
                    'id'      : 2,
                    'title'   : 'testTitle2',
                    'nickname': 'userTest',
                    'content' : 'testContent2',
                    'tags'    : [
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
                    'views'      : 2,
                    'like_status': True,
                    'status'     : 'in_posting'
                }
            ]
        )
        
    def test_success_list_post_with_offset_limit_out_of_data_range(self):
        offset = '10'
        limit  = '2'
        
        response = self.f_client\
                       .get(f'/api/posts?offset={offset}&limit={limit}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
    
    """
    실패 케이스 테스트코드
    """
    
    def test_fail_list_post_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        response = self.client\
                       .get('/api/posts', content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )