from drf_yasg       import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions
from django.urls    import path, re_path, include


"""
Swagger settings
"""
schema_view = get_schema_view(
    openapi.Info(
        title           = 'sns API',
        default_version = 'v1',
        description     = 'sns-project',
    ),
    public = True,
    permission_classes = (permissions.AllowAny,),
)

"""
Django app url patterns
"""
urlpatterns = [
    path('api/users', include('users.urls')),
    path('api/posts', include('posts.urls')),
]

"""
Swagger url patterns
"""
urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0),name='schema-json',),
    re_path(r'^swagger$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]