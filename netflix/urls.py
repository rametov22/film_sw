from django.urls import path
from .swagger import *
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter


class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={200: openapi.Response("Token is successfully retrieved.")},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


router = DefaultRouter()
router.register(r'movies', MovieDetailViewSet, basename='movie-detail')


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('actors/', ActorListCreateApiView.as_view(), name='actor-list-create'),
    path('actors/<int:pk>/', ActorDetailAPIView.as_view(), name='actor-detail'),
    path('movies/', MovieListCreateAPIView.as_view(), name='movie-list-create'),
    path('comment/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comment/<int:pk>/', CommentDetailAPIView.as_view(), name='commment-detail'),
    path('user-comments/', UserCommentListAPIView.as_view(), name='user-commment-list'),
    path('register/', CustomRegisterView.as_view(), name='api_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='api_token_auth'),
    path('logout/', CustomLogoutView.as_view(), name='api_logout'),
]


urlpatterns += router.urls
