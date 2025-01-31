from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import (
    index, MovieListView, MovieDetailView,
    ReviewListView, ReviewDetailView, toggle_like,
    ReviewUpdateView, MovieRecommendationUpdateView, MovieRecommendationDetailView,
    ReviewDeleteView, MovieRecommendationDeleteView, MovieListAPIView
)


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('main:index')
        self.assertEqual(resolve(url).func, index)

    def test_movie_list_url_resolves(self):
        url = reverse('main:movie_list')
        self.assertEqual(resolve(url).func.view_class, MovieListView)

    def test_movie_detail_url_resolves(self):
        url = reverse('main:movie_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, MovieDetailView)

    def test_review_list_url_resolves(self):
        url = reverse('main:review_list')
        self.assertEqual(resolve(url).func.view_class, ReviewListView)

    def test_review_detail_url_resolves(self):
        url = reverse('main:review_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, ReviewDetailView)

    def test_toggle_like_url_resolves(self):
        url = reverse('main:toggle_like', args=[1])
        self.assertEqual(resolve(url).func, toggle_like)

    def test_review_update_url_resolves(self):
        url = reverse('main:review_update', args=[1])
        self.assertEqual(resolve(url).func.view_class, ReviewUpdateView)

    def test_movie_recommendation_update_url_resolves(self):
        url = reverse('main:movie_recommendation_update', args=[1])
        self.assertEqual(resolve(url).func.view_class, MovieRecommendationUpdateView)

    def test_movie_recommendation_detail_url_resolves(self):
        url = reverse('main:movie_recommendation_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, MovieRecommendationDetailView)

    def test_review_delete_url_resolves(self):
        url = reverse('main:review_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, ReviewDeleteView)

    def test_movie_recommendation_delete_url_resolves(self):
        url = reverse('main:movie_recommendation_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, MovieRecommendationDeleteView)

    def test_api_movies_url_resolves(self):
        url = reverse('main:api_movies')
        self.assertEqual(resolve(url).func.view_class, MovieListAPIView)

