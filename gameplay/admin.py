from django.contrib import admin

# Register your models here.

from .models import Game, Move

# This is very basic registration with the default auto-generated view
admin.site.register(Move)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """
    This is advanced register with the custom view
    """
    list_display = ('id', 'first_player', 'second_player', 'status')



