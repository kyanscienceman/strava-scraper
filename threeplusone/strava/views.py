from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from regression import average_marathon_time

def home(request):
    return render(request, 'strava/home.html', {})

class SearchForm(forms.Form):
    age = forms.IntegerField(label='age', required=False)
    sex = forms.ChoiceField(label='sex', choices=[('M', 'M'), ('F', 'F')], required=False)

def input(request):
    return render(request, 'strava/input.html', {'form': SearchForm()})

def results(request):
    context = {}
    if request.method == 'GET':
        if not request.GET:
            context['error'] = "Sorry, you didn't conduct a search. Try again?"
        else:
            age = int(request.GET['age'])
            sex = request.GET['sex']
            context['age'] = age
            context['sex'] = sex
            context['avg_time'] = average_marathon_time(age=age, sex=sex)
    return render(request, 'strava/results.html', context)


