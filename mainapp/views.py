from django.shortcuts import render


def index(request):
    return render(request, 'mainapp/index.html')

def profile(request):
    context = {'user': request.user.social_auth.get(provider='eveonline')}
    return render(request, 'accounts/profile.html', context)

