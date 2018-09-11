import django
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.


GAME_STATUS = (
    ('F', 'First Player To Move'),
    ('S', 'Second Player To Move'),
    ('W', 'First Player Wins'),
    ('L', 'Second Player Wins'),
    ('D', 'Draw')
)


class GamesQuerySet(models.QuerySet):
    """
    Implements basic Repository-style logic to avoid writing data-related stuff in controllers
    Invoked by adding to the Game() class via as_manager() method.
    """

    def get_games_for(self, user):
        """
        Returns all games for specified user.
        :param user: user object to look for as auth.model.user
        :return: list of all games where user takes part as QuerySet.
        """
        return self.filter(
            Q(first_player=user) | Q(second_player=user)
        )

    def active(self):
        return self.filter(
            Q(status='F') | Q(status='S')
        )


class Game(models.Model):
    first_player = models.ForeignKey(User, related_name="games_first_player", on_delete=models.DO_NOTHING)
    second_player = models.ForeignKey(User, related_name="games_second_player", on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=GAME_STATUS)
    objects = GamesQuerySet.as_manager()

    def __str__(self):
        return "{0} vs {1}".format(self.first_player, self.second_player)


class Move(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    comment = models.CharField(max_length=300, blank=True)
    by_first_player = models.BooleanField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return "Move N{0} from the game {1}".format(self.pk, self.game)
