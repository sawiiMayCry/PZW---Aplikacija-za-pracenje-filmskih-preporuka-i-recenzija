from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    MovieListView, MovieDetailView,
    ReviewListView, ReviewDetailView,
    toggle_like, ReviewUpdateView, MovieRecommendationUpdateView, MovieRecommendationDetailView, ReviewViewSet, MovieListAPIView
)

app_name = 'main'  # here for namespacing of urls.

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('reviews_detail/', ReviewListView.as_view(), name='review_list'),
    path('reviews_detail/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('logged/', views.logged_in, name='logged_in'),
    path('reviews/', views.reviews, name='reviews'),
    path('toggle_like/<int:movie_id>/', toggle_like, name='toggle_like'),
    path('reviews/update/<int:pk>/', ReviewUpdateView.as_view(), name='review_update'),
    path('recommendations/update/<int:pk>/', MovieRecommendationUpdateView.as_view(), name='movie_recommendation_update'),
    path('recommendations/<int:pk>/', MovieRecommendationDetailView.as_view(), name='movie_recommendation_detail'),
    path('reviews/delete/<int:pk>/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('recommendations/delete/<int:pk>/', views.MovieRecommendationDeleteView.as_view(), name='movie_recommendation_delete'),
    path('api/', include(router.urls)),
    path('api/movies/', MovieListAPIView.as_view(), name='api_movies'),
]