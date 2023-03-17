from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from .algo import Algo
import random

from .form import PlayerForm

def app(request):
    form_disabled = False
    message = ""
    algo = Algo()
    start = algo.multiplayerGame()
   
    users_list = request.session.get('users_list', [])

    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            # check if the name is already in the users_list
            if name not in users_list:
                users_list.append(name)
            request.session['users_list'] = users_list  # store the updated users_list in the session
            # disable the form if the limit is reached or exceeded
            form_disabled = len(users_list) >= 5
            form = PlayerForm()
        else:
            form_disabled = False
            message = "Le formulaire est invalide"
    else:
        form_disabled = False
        form = PlayerForm()
        message = ""

    context = {
        'form_key': form,
        'users_list': users_list[:5],  # limit the list to 5 names maximum
        'form_disabled': form_disabled,
        'message': message,
        'algo' : algo
    }
    return render(request, 'form.html', context)


def reset(request):
    request.session.clear()
    return redirect('app')
