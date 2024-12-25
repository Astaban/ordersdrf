from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username')
    list_display_links = ('username', )
    ordering = ('username', )
    list_per_page = 25
    save_on_top = True

