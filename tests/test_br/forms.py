from django.forms import ModelForm

from .models import BrCitizen


class BrCitizenForm(ModelForm):
    class Meta(object):
        model = BrCitizen
        fields = ('cpf', 'cpf_optional')
