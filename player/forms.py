from django.forms import ModelForm

from .models import Invitation

class InvitationForm(ModelForm):
    """
    This class is auto-generated for for invitations based on ModelForm
    """
    class Meta:
        """
        This class is a configuration for the ModelForm we just declared
        """
        model = Invitation
        exclude = ('from_user', 'timestamp')