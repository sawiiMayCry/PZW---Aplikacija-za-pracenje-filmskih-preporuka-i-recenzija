from django.urls import path
from . import views
from .views import (
    MovieListView, MovieDetailView,
    ReviewListView, ReviewDetailView,
)

app_name = 'main'  # here for namespacing of urls.

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
]