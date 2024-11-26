from django.contrib import admin
from .models import *

# Register your models here.

model_list = [Movie, Review, UserMovie, UserRecommendation, MovieRecommendation]
admin.site.register(model_list)