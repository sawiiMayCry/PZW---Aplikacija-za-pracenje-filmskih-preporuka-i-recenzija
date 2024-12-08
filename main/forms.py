from django import forms
from main.models import Review, MovieRecommendation


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['movie', 'rating', 'comment']
        widgets = {
            'movie': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class RecommendationForm(forms.ModelForm):
    class Meta:
        model = MovieRecommendation
        fields = ['movie', 'reason']
        widgets = {
            'movie': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
