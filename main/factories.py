# main/factories.py
import factory
from django.contrib.auth.models import User
from .models import Movie, Review, UserMovie, UserRecommendation, MovieRecommendation
from factory import Faker, SubFactory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('user_name')
    email = Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie


    title = Faker('sentence')
    release_date = Faker('date_this_century')
    genre = Faker('word')
    description = Faker('paragraph')
    director = Faker('name')


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    user = SubFactory(UserFactory)
    movie = SubFactory(MovieFactory)
    rating = Faker('random_int', min=1, max=10)
    comment = Faker('text')
    created_at = Faker('date_this_year')


class UserMovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserMovie

    user = SubFactory(UserFactory)
    movie = SubFactory(MovieFactory)
    liked = Faker('boolean')


class UserRecommendationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserRecommendation

    user = SubFactory(UserFactory)
    movie = SubFactory(MovieFactory)
    reason = Faker('text')


class MovieRecommendationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MovieRecommendation

    movie = SubFactory(MovieFactory)
    user = SubFactory(UserFactory)
    reason = Faker('text')
