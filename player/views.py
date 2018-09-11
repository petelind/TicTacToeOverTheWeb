from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404

from player.models import Invitation
from .forms import InvitationForm

# Create your views here.
from gameplay.models import Game


@login_required()
def home(request: HttpRequest):
    """
    Contains logic which will render Home for the Player
    :param request: request sent to the controller as HttpRequest
    :return renders view via home.html & Dict of all Games of the currently logged user
    """
    try:
        my_games = Game.objects.get_games_for(request.user)
        my_active_games = my_games.active()
        invitations = request.user.invitations_received.all()

        return render(request, 'player/home.html',
                      {
                          'games': my_active_games,
                          'invitations': invitations
                      })

    except Exception as e:
        """
        log an error in the HD Insights, CloudWatch or whatever service you prefer:
        
        logger = logging.getLogger(__name__)
        logger.error('ALERT: home() in the player() failed, details :' + e.message, e.args)
        """



@login_required()
def new_invitation(request: HttpRequest):
    """
    Displays an InvitationForm for filling out on GET,
    redirects to Home() on POST success,
    redirects back to the form with validation errors on POST if validation failed
    :param request:
    :return: Form() in the Context() on validation error, redirect to Home() on success
    """
    if request.method == 'POST':
        # dont forget - form does not display "from" in the invitation, lets fill it:
        invitation = Invitation(from_user=request.user)
        form = InvitationForm(instance=invitation, data=request.POST)
        # now form shall be fine - all fields present. Lets check if input is indeed ok:
        if form.is_valid():
            form.save()
            return redirect('player_home')
    else:
        form = InvitationForm()

    return render(request, 'player/new_invitation_form.html', {'form': form})

@login_required()
def accept_invitation(request: HttpRequest, id: int):
    """
    Displays a page which allows to Accept or Reject invitation
    :param request: request as HttpRequest
    :param id: id of the invitation to be accepted / rejected
    :return: page for the Invitation, 404 if no such invitation,
    or raises PermissionDenied if user tries to access other users Invitation
    """
    invitation = get_object_or_404(Invitation, pk=id)
    if not request.user == invitation.to_user:
        raise PermissionDenied
    if request.method == 'POST':
        if 'accept' in request.POST:
            game = Game.objects.create(
                first_player=invitation.to_user,
                second_player=invitation.from_user
            )
        invitation.delete()
        return redirect('player_home')
    else:
        return render(
            request,
            'player/accept_invitation_form.html',
            {'invitation': invitation}
        )

