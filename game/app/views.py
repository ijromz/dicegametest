from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .form import PlayerForm

users_list = []

def app(request):

    form_disabled = False  # initial value of form_disabled
    if request.method == 'POST': 
        form = PlayerForm(request.POST)
        if form.is_valid():
            users_list.append(form.cleaned_data['name'])
            if len(users_list) >= 5:  # check if number of names is greater than or equal to 5
                form_disabled = True  # disable form if limit is reached
            form = PlayerForm()
        else:
            message = "Le formulaire est invalide"
    else:
        form = PlayerForm()
        message = ""

    context = {
        'form_key': form,
        'users_list' : users_list,
        'form_disabled': form_disabled  # add form_disabled to context
    }
    return render(request, 'form.html', context)

