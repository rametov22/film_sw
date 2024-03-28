from django.db import models
from django.contrib.auth.models import User
from .validators import *
# Create your models here.


class Actor(models.Model):
    name = models.CharField(max_length=255, validators=[starts_with_uppercase_validator, contains_only_letters_validator])
    date_birth = models.DateField(verbose_name='date_birth', validators=[age_validator])

    def __str__(self):
        return self.name


class Movie(models.Model):
    actors = models.ManyToManyField(Actor, 'актеры')
    name = models.CharField(max_length=255, validators=[contains_only_letters_validator])
    date_created = models.DateField(validators=[age_validator])

    def __str__(self):
        return self.name


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'


