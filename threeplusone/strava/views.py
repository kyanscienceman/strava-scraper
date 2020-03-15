from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from regression import regressions, get_panel_regression
import numpy as np

RACE_IDS = {
    'BS19': '2019 Boston Marathon', 
    'BS18': '2018 Boston Marathon',
    'BS17': '2017 Boston Marathon', 
    'BS16': '2016 Boston Marathon',
    'BS15': '2015 Boston Marathon', 
    'BS14': '2014 Boston Marathon',
    'CH19': '2019 Chicago Marathon',
    'CH18': '2018 Chicago Marathon',
    'CH17': '2017 Chicago Marathon',
    'CH16': '2016 Chicago Marathon',
    'CH15': '2015 Chicago Marathon',
    'CH14': '2014 Chicago Marathon',
    'NY19': '2019 New York Marathon',
    'NY18': '2018 New York Marathon',
    'NY17': '2017 New York Marathon',
    'NY16': '2016 New York Marathon',
    'NY15': '2015 New York Marathon',
    'NY14': '2014 New York Marathon'
}

class SearchForm(forms.Form):
    race = forms.ChoiceField(label='Race', required=False, choices=[('', '---')]\
        +[(r, RACE_IDS[r]) for r in sorted(RACE_IDS)])
    age = forms.IntegerField(label='Age', required=False)
    sex = forms.ChoiceField(label='Sex', choices=[
        ('', '---'), ('M', 'M'), ('F', 'F')
    ], required=False)

def home(request):
    return render(request, 'strava/home.html', {})

def findings(request):
    res = get_panel_regression()
    regcoef = 100 * (1 - np.exp(res.params[0]))
    return render(request, 'strava/findings.html', {
        'nobs': res.nobs,
        'regcoef': regcoef
    })

def input(request):
    return render(request, 'strava/input.html', {'form': SearchForm()})

def results(request):
    context = {}
    if request.method == 'GET':
        if not request.GET:
            context['error'] = "Sorry, you didn't conduct a search. Try again?"
            context['form'] = SearchForm()
            return render(request, 'strava/input.html', context)

        age = None
        sex = None
        race = None
        if request.GET['age']:
            age = int(request.GET['age'])
            context['age'] = age
        if request.GET['sex']:
            sex = request.GET['sex']
            context['sex'] = sex
        if request.GET['race']:
            race = request.GET['race']
            context['race'] = RACE_IDS[race]
        context['regcoef'] = 100 * (1 - regressions(age=age, sex=sex, race=race))
        context['linearfit'] = 'images/linearfit.png'
        context['hist'] = 'images/hist.png'

        return render(request, 'strava/results.html', context)


