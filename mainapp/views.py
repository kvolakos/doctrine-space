from django.shortcuts import render
from django.contrib.auth import logout


def index(request):
    return render(request, 'mainapp/index.html')

def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'mainapp/index.html')

    User = request.user.social_auth.get(provider='eveonline')
    context = {'User': User}

    return render(request, 'accounts/profile.html', context)

def logout_view(request):
    logout(request)
    return render(request, 'mainapp/index.html')


