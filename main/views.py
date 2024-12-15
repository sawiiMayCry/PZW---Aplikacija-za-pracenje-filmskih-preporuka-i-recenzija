from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Movie, UserMovie, UserRecommendation, Review, MovieRecommendation
from main.forms import ReviewForm, RecommendationForm
from django.views.generic import ListView, DetailView
from django.db.models import Q

# Create your views here.

# ListView za Movie s pretraživanjem
class MovieListView(ListView):
    model = Movie
    template_name = 'main/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 10  # Dodano za page

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(genre__icontains=search_query))
        return queryset

# DetailView za Movie
class MovieDetailView(DetailView):
    model = Movie
    template_name = 'main/movie_detail.html'
    context_object_name = 'movie'

# ListView za Review s pretraživanjem i filtriranjem po korisniku
class ReviewListView(ListView):
    model = Review
    template_name = 'main/review_list.html'
    context_object_name = 'reviews_detail'

    def get_queryset(self):
        queryset = super().get_queryset()
        user_filter = self.request.GET.get('user', '')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)
        return queryset

# DetailView za Review
class ReviewDetailView(DetailView):
    model = Review
    template_name = 'main/review_detail.html'
    context_object_name = 'review'

    
def index(request):
    return render(request, 'main/index.html')

# pogled za login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Prijavljuje korisnika
            return redirect('logged_in')  # na logged_in stranicu nakon prijave
    else:
        form = AuthenticationForm()

    return render(request, 'main/login.html', {'form': form})

# pogled za logout
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def logged_in(request):
    """
    Funkcionalnost za prikazivanje logged.html
    Samo prijavljeni korisnici mogu pristupiti ovoj stranici.
    """
    movies = Movie.objects.all()
    liked_movies = UserMovie.objects.filter(user=request.user, liked=True).select_related('movie')
    user_recommendations = UserRecommendation.objects.filter(user=request.user).select_related('movie')  # Preporuke za korisnika

    return render(request, 'main/logged.html', {
        'all_movies': movies,
        'liked_movies': liked_movies,
        'user_recommendations': user_recommendations,
    }) 

@login_required
def reviews(request):
    """
    Dohvat svih recenzija i preporuka za trenutnog korisnika.
    """
    # Dohvati sve recenzije iz baze
    reviews = Review.objects.all()
    
    # Dohvati sve preporuke za trenutnog korisnika
    movie_recommendations = MovieRecommendation.objects.all()

    # Ako se podaci šalju preko POST-a, obrađujemo ih
    if request.method == 'POST':
        if 'submit_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('main:reviews')
        else:
            review_form = ReviewForm()
        
        if 'submit_recommendation' in request.POST:
            recommendation_form = RecommendationForm(request.POST)
            if recommendation_form.is_valid():
                recommendation = recommendation_form.save(commit=False)
                recommendation.user = request.user
                recommendation.save()
                return redirect('main:reviews')
        else:
            recommendation_form = RecommendationForm()
    else:
        review_form = ReviewForm()
        recommendation_form = RecommendationForm()

    return render(request, 'main/reviews.html', {
        'reviews': reviews,
        'movie_recommendations': movie_recommendations,
        'review_form': review_form,
        'recommendation_form': recommendation_form,
    })