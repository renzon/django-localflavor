from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _

from localflavor.br.forms import CPFFormField
from localflavor.br.validators import CPF_LEN, validate_cpf, remove_cpf_non_digits

from .br_states import STATE_CHOICES


class BRStateField(CharField):
    """A model field for states of Brazil."""

    description = _("State of Brazil (two uppercase letters)")

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = STATE_CHOICES
        kwargs['max_length'] = 2
        super(BRStateField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(BRStateField, self).deconstruct()
        del kwargs['choices']
        return name, path, args, kwargs


class CPFField(CharField):
    description = _('Brazilian cpf number')
    default_validators = CharField.default_validators + [validate_cpf]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = CPF_LEN
        super(CPFField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        value = remove_cpf_non_digits(value)
        return super(CPFField, self).get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': CPFFormField}
        defaults.update(kwargs)
        return super(CPFField, self).formfield(**defaults)
