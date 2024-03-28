from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, viewsets
from drf_yasg import openapi
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Actor, Movie, Comment
from django.http import Http404
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, permission_classes, action
from .serializers import *
# Create your views here.


# Actor List and Create
class ActorListCreateApiView(APIView):
    def get(self, request):
        actors = Actor.objects.all()
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ActorSerializer)
    def post(self, request):
        if request.user.is_superuser:
            """
            new actor
            """
            serializer = ActorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('вы не можете добавялть', status=status.HTTP_403_FORBIDDEN)


# Actor Update and Delete
class ActorDetailAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get_actor(self, pk):
        try:
            return Actor.objects.get(pk=pk)
        except Actor.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        actor = self.get_actor(pk)
        serializer = ActorSerializer(actor)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ActorSerializer)
    def put(self, request, pk):
        """

        update

        """
        actor = self.get_actor(pk)
        serializer = ActorSerializer(actor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        actor = self.get_actor(pk)
        actor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Movie List and Create
class MovieListCreateAPIView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MovieCreateSerializer)
    def post(self, request):
        if request.user.is_superuser:
            """
    
            new movie
    
            """
            serializer = MovieCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Вы не можете добавлять фильмы', status=status.HTTP_403_FORBIDDEN)


# Movie Update and Delete
class MovieDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_movie(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        movie = self.get_movie(pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MovieSerializer)
    def put(self, request, pk):
        """

        update

        """
        movie = self.get_movie(pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = self.get_movie(pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'actor_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ))
    @action(detail=True, methods=['post'])
    def add_actor(self, request, pk=None):
        movie = self.get_object()
        actor_id = request.data.get('actor_id')
        if actor_id:
            try:
                actor = Actor.objects.get(pk=actor_id)
            except Actor.DoesNotExist:
                return Response({'error': 'Actor with specified ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

            movie.actors.add(actor)
            movie.save()
            serializer = self.get_serializer(movie)
            return Response(serializer.data)
        else:
            return Response({'error': 'Actor ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'actor_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ))
    @action(detail=True, methods=['post'])
    def remove_actor(self, request, pk=None):
        movie = self.get_object()
        actor_id = request.data.get('actor_id')
        if actor_id:
            try:
                actor = Actor.objects.get(pk=actor_id)
            except Actor.DoesNotExist:
                return Response({'error': 'Actor with specified ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

            movie.actors.remove(actor)
            movie.save()
            serializer = self.get_serializer(movie)
            return Response(serializer.data)
        else:
            return Response({'error': 'Actor ID is required'}, status=status.HTTP_400_BAD_REQUEST)


# comment List and Create
class CommentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CommentCreateSerializer)
    def post(self, request):
        if request.user.is_authenticated:
            serializer = CommentCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('авторизуйтесь', status=status.HTTP_403_FORBIDDEN)


# comment Update and Delete
class CommentDetailAPIView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get_comment(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        comment = self.get_comment(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CommentUpdateSerializer)
    def put(self, request, pk):
        """

        update

        """
        comment = self.get_comment(pk)
        self.check_object_permissions(request, comment)
        serializer = CommentUpdateSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_comment(pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# User Comment List
class UserCommentListAPIView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserCommentSerializer(user)
        return Response(serializer.data)


# User register logout
class CustomRegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'логин или пароль не введен'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Логин уже занят'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'Регистрация успешно'}, status=status.HTTP_201_CREATED)


class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_authenticated:
            token = Token.objects.filter(user=request.user).first()
            if token:
                token.delete()
                return Response({'message': 'Успешный выход'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Токен пользователя не найден'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Пользователь не аутентифицирован'}, status=status.HTTP_401_UNAUTHORIZED)


    #
    # @swagger_auto_schema(method='post', request_body=AddActorSerializer)
    # @action(detail=True, methods=['post'])
    # def add_actor(self, request, pk=None):
    #     movie = self.get_movie(pk)
    #     actor_id = request.data.get('actor_id')
    #     if actor_id:
    #         actor = Actor.objects.get(pk=actor_id)
    #         movie.actors.add(actor)
    #         movie.save()
    #         serializer = AddActorSerializer()
    #         return Response(serializer.data)
    #     else:
    #         return Response({'error': 'Actor id is required'}, status=status.HTTP_400_BAD_REQUEST)
    #
    # @swagger_auto_schema(request_body=AddActorSerializer)
    # @action(detail=True, methods=['post'])
    # def remove_actor(self, request, pk=None):
    #     movie = self.get_movie(pk)
    #     actor_id = request.data.get('actor_id')
    #     if actor_id:
    #         actor = Actor.objects.get(pk=actor_id)
    #         movie.actors.remove(actor)
    #         movie.save()
    #         serializer = AddActorSerializer(movie)
    #         return Response(serializer.data)
    #     else:
    #         return Response({'errors': 'Actor id is required'}, status=status.HTTP_400_BAD_REQUEST)
