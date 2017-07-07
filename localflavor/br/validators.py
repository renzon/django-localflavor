# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

CPF_LEN = 11
_re_match_numeric_chars = re.compile(r'[^0-9]')


def validate_digits_only(cpf):
    if not cpf.isdigit():
        raise ValidationError(_('Must contain only digits.'), 'digits')


def validate_has_exactly_len(cpf, n):
    if len(cpf) != n:
        raise ValidationError(
            _('Must have exactly {number} digits.').format(number=n),
            'length'
        )


def remove_non_digits(s):
    return _re_match_numeric_chars.sub('', s)


def _dv_maker(v):
    v %= 11
    if v >= 2:
        return 11 - v
    return 0


def validate_cpf(cpf):
    validate_digits_only(cpf)
    validate_has_exactly_len(cpf, CPF_LEN)
    orig_dv = cpf[-2:]
    orig_cpf = cpf[:]
    new_1dv = sum(
        [i * int(cpf[idx]) for idx, i in enumerate(range(10, 1, -1))])
    new_1dv = _dv_maker(new_1dv)
    cpf = cpf[:-2] + str(new_1dv) + cpf[-1]
    new_2dv = sum(
        [i * int(cpf[idx]) for idx, i in enumerate(range(11, 1, -1))])
    new_2dv = _dv_maker(new_2dv)
    cpf = cpf[:-1] + str(new_2dv)
    if cpf[-2:] != orig_dv:
        raise ValidationError(_('Invalid CPF number.'))

    return orig_cpf
