from django.db import models

from localflavor.br.models import CPFField


class BrCitizen(models.Model):
    cpf = CPFField()
    cpf_optional = CPFField(blank=True)
