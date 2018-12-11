from django.shortcuts import render
from django.contrib.auth import logout
import requests as r
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from mainapp.forms import FitCreationForm
from mainapp.models import Fitting, Invtypes
import sys


def index(request):
    return profile(request)


def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'mainapp/index.html')

    User = request.user.social_auth.get(provider='eveonline')
    userdata = r.get('https://esi.evetech.net/latest/characters/' + str(User.uid))
    corp_id = userdata.json()['corporation_id']
    # alliance_id = userdata.json()['alliance_id']
    corp_name = r.get('https://esi.evetech.net/latest/corporations/' + str(corp_id)).json()['name']
    # alliance_name = r.get('https://esi.evetech.net/latest/alliances/' + str(alliance_id)).json()['name']
    corporation = {'id': corp_id, 'name': corp_name}
    # alliance = {'id': alliance_id, 'name': alliance_name}

    fittings = Fitting.objects.filter(author=request.user)

    context = {'User': User,
               'corp': corporation,
               # 'alliance': alliance,
               'fittings': fittings}

    return render(request, 'accounts/profile.html', context)


def logout_view(request):
    logout(request)
    return render(request, 'mainapp/index.html')


def fitting(request):
    if request.method == 'POST':
        form = FitCreationForm(request.POST)

        if form.is_valid():
            fit_name = form.cleaned_data['fit_name']
            fitstring = form.cleaned_data['fit_text']
            fit_text = form.cleaned_data['fit_text'].split("\n\r")
            ship_name = fit_text[0].split(',')[0][1:]
            ship_id = Invtypes.objects.get(typename__exact=ship_name).typeid
            f = Fitting(name=fit_name, author=request.user, ship_name=ship_name, ship_id=ship_id, fitstring=fitstring)
            f.save()

            url = "/mainapp/fitting/?id={0}".format(f.id)
            return HttpResponseRedirect(url)

    elif request.method == 'GET' and request.GET.get('id'):
        fit_id = request.GET.get('id')

        fit = get_object_or_404(Fitting, id__exact=fit_id)
        fitstring = fit.fitstring
        if fit.author == request.user:
            if fitstring:
                fit_text = fitstring.split("\n\r")
                highs = fit_text[3].split("\n")
                mids = fit_text[2].split("\n")
                lows = fit_text[1].split("\n")
                rigs = fit_text[4].split("\n")

                context = {'fit': fit,
                           'User': request.user.social_auth.get(provider='eveonline'),
                           'highs': highs,
                           'mids': mids,
                           'lows': lows,
                           'rigs': rigs}
                return render(request, 'mainapp/fit.html', context)
            else:
                return render(request, 'mainapp/fitnotfound.html')
        else:
            return render(request, 'mainapp/fitnotfound.html')
    else:
        form = FitCreationForm()

    return render(request, 'mainapp/fitting.html', {'form': form})


def get_fitting(request):
    fit_id = request.GET.get('id')

    fit = Fitting.objects.get(id__exact=fit_id)
    if fit.author == request.user:
        return HttpResponse(fit.name)
    else:
        return HttpResponse("nah")




