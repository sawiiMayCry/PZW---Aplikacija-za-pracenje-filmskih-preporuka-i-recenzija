from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

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
    return render(request, 'main/logged.html')