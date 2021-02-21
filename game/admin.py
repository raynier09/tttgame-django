from django.contrib import admin
from .models import *

# This will register the two models in Django Administration
admin.site.register(Game)
admin.site.register(Leaderboard)