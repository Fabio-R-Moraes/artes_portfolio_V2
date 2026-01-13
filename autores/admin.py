from django.contrib import admin
from autores.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...