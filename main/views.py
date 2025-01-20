from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Movie, UserMovie, UserRecommendation, Review, MovieRecommendation
from main.forms import ReviewForm, RecommendationForm
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ReviewSerializer
from rest_framework.generics import ListAPIView
from .serializers import MovieSerializer

# Create your views here.

class MovieListAPIView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]  


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    """ Za prikazivanje samo komentara ulogiranog korisnika
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    """
    

    def perform_create(self, serializer):
        # Automatski postavljamo korisnika kao autora recenzije
        serializer.save(user=self.request.user)


# Brisanje preporuka
class MovieRecommendationDeleteView(LoginRequiredMixin, DeleteView):
    model = MovieRecommendation
    template_name = 'main/movie_recommendation_confirm_delete.html'
    context_object_name = 'recommendation'
    success_url = reverse_lazy('main:reviews')  # Preusmjeravanje na popis preporuka nakon brisanja

    def get_queryset(self):
        # samo korisnici koji su dali preporuku mogu je obrisati
        return self.model.objects.filter(user=self.request.user)


# Brisanje recenzija
class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'main/review_confirm_delete.html'
    context_object_name = 'review'
    success_url = reverse_lazy('main:review_list')  # Preusmjeravanje na popis recenzija nakon brisanja

    def get_queryset(self):
        # samo korisnici koji su napisali recenziju mogu je obrisati
        return self.model.objects.filter(user=self.request.user)
    

class MovieRecommendationUpdateView(UpdateView):
    model = MovieRecommendation
    template_name = 'main/movie_recommendation_update.html'
    fields = ['reason']  # Polje koje korisnik može ažurirati
    context_object_name = 'recommendation'

    def test_func(self):
        # Provjera da li je korisnik vlasnik recenzije
        return self.request.user == self.get_object().user


    def get_success_url(self):
        # Preusmjeravanje na DetailView ažuriranog objekta
        return reverse('main:movie_recommendation_detail', kwargs={'pk': self.object.pk})

class ReviewUpdateView(UpdateView):
    model = Review
    template_name = 'main/review_update.html'
    fields = ['rating', 'comment']  # Polja koja korisnik može ažurirati
    

    def test_func(self):
        # Provjera da li je korisnik vlasnik recenzije
        return self.request.user == self.get_object().user

    def get_success_url(self):
        # Preusmjeravanje na DetailView ažuriranog objekta
        return reverse('main:review_detail', kwargs={'pk': self.object.pk})
    


# ListView za Movie s pretraživanjem
class MovieListView(ListView):
    model = Movie
    template_name = 'main/movie_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        genre_filter = self.request.GET.get('genre', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(genre__icontains=search_query)
            )
        if genre_filter:
            queryset = queryset.filter(genre__icontains=genre_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Movie.objects.values_list('genre', flat=True).distinct()
        return context

# DetailView za Movie
class MovieDetailView(DetailView):
    model = Movie
    template_name = 'main/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()  # Prikazivanje svih recenzija za ovaj film
        context['movie_recommendations'] = self.object.movie_recommendations.all()  # Prikazivanje svih preporuka za ovaj film
        if self.request.user.is_authenticated:
            # Provjeri je li korisnik lajkao film
            liked = UserMovie.objects.filter(
                user=self.request.user, movie=self.object, liked=True
            ).exists()
            context['liked'] = liked
        else:
            context['liked'] = False
        return context

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

# DetailView za recenzije
class ReviewDetailView(DetailView):
    model = Review
    template_name = 'main/review_detail.html'
    context_object_name = 'review'

    
def index(request):
    return render(request, 'main/index.html')

#DetailView za preporuke
class MovieRecommendationDetailView(DetailView):
    model = MovieRecommendation
    template_name = 'main/movie_recommendation_detail.html'
    context_object_name = 'recommendation'

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

@login_required
def toggle_like(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user_movie, created = UserMovie.objects.get_or_create(user=request.user, movie=movie)

    # If liked unlike, else (unliked) like
    if user_movie.liked:
        user_movie.liked = False
    else:
        user_movie.liked = True

    user_movie.save()
    return redirect('main:movie_detail', pk=movie_id)