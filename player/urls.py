from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import home, new_invitation, accept_invitation

urlpatterns = [
    url('home', home, name='player_home'),
    url('new_invitation', new_invitation, name='player_new_invitation'),
    url('login', LoginView.as_view(template_name='player/login_form.html'), name='player_login'),
    url('logout', LogoutView.as_view(template_name='player/logout_confirmation.html'), name='player_logout'),
    path('accept_invitation/<int:id>', accept_invitation, name='player_accept_invitation'),
]
