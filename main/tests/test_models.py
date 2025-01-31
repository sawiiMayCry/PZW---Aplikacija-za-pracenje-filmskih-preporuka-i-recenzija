from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Movie, Review

class TestReviewModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
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
            rating=9,
            comment="komentar"
        )

    def test_review_creation(self):
        self.assertEqual(self.review.user.username, "testuser")
        self.assertEqual(self.review.movie.title, "some-movie")
        self.assertEqual(self.review.rating, 9)
        self.assertEqual(str(self.review), "testuser - some-movie - 9/10")
