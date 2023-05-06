from django import forms
from django.forms.models import inlineformset_factory

from .models import GuardObject, GuardPost


class GuardObjectForm(forms.ModelForm):
    class Meta:
        model = GuardObject
        exclude = ('contract', 'qteam',)

class BaseGuardPostForm(forms.ModelForm):
    class Meta:
        model = GuardPost
        exclude = ('guard_object', 'personnel',)
        widgets = {
            'number': forms.NumberInput(attrs={'style': 'width:50px'}),
            'note': forms.Textarea(attrs={'rows': 2,'cols': 65})
            }

class GuardPostForm(forms.ModelForm):
    class Meta:
        model = GuardPost
        exclude = ('guard_object',)