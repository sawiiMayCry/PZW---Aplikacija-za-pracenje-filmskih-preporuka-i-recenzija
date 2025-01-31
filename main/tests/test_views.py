from rest_framework.test import APIClient
from django.test import TestCase
from main.models import Review, Movie, UserMovie, MovieRecommendation
from django.contrib.auth.models import User
from django.urls import reverse

from django.urls import reverse

class ToggleLikeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.movie = Movie.objects.create(
            title="some-movie",
            release_date="2010-07-16",
            genre="some-genre",
            description="some-description",
            director="some-director"
        )

    def test_toggle_like(self):
        response = self.client.get(reverse('main:toggle_like', args=[self.movie.pk]))
        self.assertRedirects(response, reverse('main:movie_detail', args=[self.movie.pk]))
        
        # Provjeri da je film sada lajkan
        self.assertTrue(UserMovie.objects.filter(user=self.user, movie=self.movie, liked=True).exists())

        # Ponovno klikni i provjeri da je film sada un-lajkan
        response = self.client.get(reverse('main:toggle_like', args=[self.movie.pk]))
        self.assertTrue(UserMovie.objects.filter(user=self.user, movie=self.movie, liked=False).exists())


class ReviewDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.movie = Movie.objects.create(
            title="some-movie",
            release_date="2010-07-16",
            genre="some-genre",
            description="some-description",
            director="some-director"
        )
        self.review = Review.objects.create(
            user=self.user,
            movie=self.movie,
            rating=8,
            comment="komentar1"
        )

    def test_review_delete_view(self):
        response = self.client.get(reverse('main:review_delete', args=[self.review.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Provjera da recenzija može biti obrisana
        response = self.client.post(reverse('main:review_delete', args=[self.review.pk]))
        self.assertRedirects(response, reverse('main:review_list'))
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())

class MovieRecommendationUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.movie = Movie.objects.create(
            title="some-movie",
            release_date="2010-07-16",
            genre="some-genre",
            description="some-description",
            director="some-director"
        )
        self.recommendation = MovieRecommendation.objects.create(
            user=self.user,
            movie=self.movie,
            reason="komenatar1"
        )

    def test_movie_recommendation_update_view(self):
        response = self.client.get(reverse('main:movie_recommendation_update', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 200)

        # Ažuriraj preporuku
        response = self.client.post(reverse('main:movie_recommendation_update', args=[self.recommendation.pk]), {
            'reason': 'azuriraniKomentar'
        })
        self.assertRedirects(response, reverse('main:movie_recommendation_detail', args=[self.recommendation.pk]))

        # Provjeri da je ažurirana preporuka
        self.recommendation.refresh_from_db()
        self.assertEqual(self.recommendation.reason, 'azuriraniKomentar')