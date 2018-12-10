from django.shortcuts import render
from django.contrib.auth import logout
import requests as r

from django.db import connection


def index(request):
    checklist = {}
    k = 782
    with connection.cursor() as cursor:
        for s in [11, 12, 13, 2663]:
            cursor.execute("SELECT * FROM invTypes JOIN dgmTypeEffects ON invTypes.typeID=dgmTypeEffects.typeID WHERE dgmTypeEffects.effectID=%s" % s)
            for i in cursor.fetchall():
                if i[1] in checklist:
                    checklist[i[1]].append(i[2])
                else:
                    checklist[i[1]] = [i[2]]
        cursor.execute("SELECT * FROM invGroups WHERE groupID=%s" % k)
        group = cursor.fetchone()
    context = {'checklist': checklist[k], 'group': group[2]}
    return render(request, 'mainapp/index.html', context)


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




