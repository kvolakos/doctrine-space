from django.shortcuts import render
from django.contrib.auth import logout
import requests as r


def index(request):
    return render(request, 'mainapp/index.html')

def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'mainapp/index.html')

    User = request.user.social_auth.get(provider='eveonline')
    userdata = r.get('https://esi.evetech.net/latest/characters/' + str(User.uid))
    corp_id = userdata.json()['corporation_id']
    alliance_id = userdata.json()['alliance_id']
    corp_name = r.get('https://esi.evetech.net/latest/corporations/' + str(corp_id)).json()['name']
    alliance_name = r.get('https://esi.evetech.net/latest/alliances/' + str(alliance_id)).json()['name']
    corporation = {'id': corp_id, 'name': corp_name}
    alliance = {'id': alliance_id, 'name': alliance_name}

    context = {'User': User, 'corp': corporation, 'alliance': alliance}

    return render(request, 'accounts/profile.html', context)

def logout_view(request):
    logout(request)
    return render(request, 'mainapp/index.html')




