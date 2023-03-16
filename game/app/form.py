from django import forms

class PlayerForm(forms.Form):
    name = forms.CharField(label='Joueur', max_length=100, required=True)

