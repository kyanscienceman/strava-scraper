from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from regression import regressions

class SearchForm(forms.Form):
    age = forms.IntegerField(label='age', required=False)
    sex = forms.ChoiceField(label='sex', choices=[
        ('', '---'), ('M', 'M'), ('F', 'F')
    ], required=False)

def home(request):
    return render(request, 'strava/home.html', {})

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
        if request.GET['age']:
            age = int(request.GET['age'])
            context['age'] = age
        if request.GET['sex']:
            sex = request.GET['sex']
            context['sex'] = sex
        context['regcoef'] = -1 * regressions(age=age, sex=sex)
        context['linearfit'] = 'images/linearfit.png'
        context['hist'] = 'images/hist.png'
        return render(request, 'strava/results.html', context)


