from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Movie, UserMovie, UserRecommendation, Review, MovieRecommendation

# Create your views here.
    
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

    return render(request, 'main/reviews.html', {
        'reviews': reviews,
        'movie_recommendations': movie_recommendations,
    })