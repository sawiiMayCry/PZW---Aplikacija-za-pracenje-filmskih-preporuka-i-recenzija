from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    description = models.TextField()
    director = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.rating}/10"


class UserMovie(models.Model):
    user = models.ForeignKey(User, related_name='liked_movies', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='liked_by_users', on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

    def __str__(self):
        return f"User {self.user} likes Movie {self.movie} - Liked: {self.liked}"


class UserRecommendation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return f"Recommendation for {self.user.username} - {self.movie.title}"


class MovieRecommendation(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_recommendations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recommendations')
    reason = models.TextField()

    def __str__(self):
        return f"Recommendation for {self.movie.title} by {self.user.username}"



