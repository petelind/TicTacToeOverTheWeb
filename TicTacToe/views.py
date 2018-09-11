from django.shortcuts import render, redirect

def welcome(request):
    """
    Renders application landing page.
    :param request: request parameters as HttpRequest()
    :return: Renders either default Home or Player's Home
    """
    if request.user.is_authenticated:
        return redirect('player_home')
    else:
        return render(request, 'player/welcome.html')
