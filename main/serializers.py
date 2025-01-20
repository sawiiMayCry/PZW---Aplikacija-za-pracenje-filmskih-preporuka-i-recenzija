from rest_framework import serializers
from .models import Review, Movie

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Ocjena mora biti između 1 i 10.")
        return value
    
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_date', 'genre', 'description', 'director']
