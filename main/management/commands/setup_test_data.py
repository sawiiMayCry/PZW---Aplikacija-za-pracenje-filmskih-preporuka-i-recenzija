import random
from random import choice
from django.core.management.base import BaseCommand
from main.models import UserMovie, Review, MovieRecommendation, UserRecommendation, Movie, User
from main.factories import UserFactory, MovieFactory, ReviewFactory, UserMovieFactory, UserRecommendationFactory, MovieRecommendationFactory

class Command(BaseCommand):
    help = 'Sets up test data for the application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        # Brisanje
        UserMovie.objects.all().delete()
        Review.objects.all().delete()
        MovieRecommendation.objects.all().delete()
        UserRecommendation.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write('Creating new data...')
        
        users = UserFactory.create_batch(5)
        
        
        movies = MovieFactory.create_batch(5)

       
        for user in users:
            for _ in range(2):
                ReviewFactory.create(user=user, movie=random.choice(movies))


        for user in users:
            user_movies = random.sample(movies, 2)
            for movie in user_movies:
                UserMovieFactory.create(user=user, movie=movie)


        selected_users = random.sample(users, 3)
        for user in selected_users:
            movie = random.choice(movies)
            UserRecommendationFactory.create(user=user, movie=movie)

        
        for _ in range(3):
            movie = random.choice(movies)
            user = random.choice(users)
            MovieRecommendationFactory.create(user=user, movie=movie)

        self.stdout.write(self.style.SUCCESS('Test data setup complete!'))
