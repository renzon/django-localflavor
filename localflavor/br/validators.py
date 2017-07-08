# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from itertools import chain

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

CPF_LEN = 11
_re_cpf_mask_chars = re.compile(r'[-\.]')


def validate_digits_only(cpf):
    if not cpf.isdigit():
        raise ValidationError(_('Must contain only digits.'), 'digits')


def validate_has_exactly_len(cpf, n):
    if len(cpf) != n:
        raise ValidationError(
            _('Must have exactly {number} digits.').format(number=n),
            'length'
        )


def remove_cpf_non_digits(s):
    if s:
        s = _re_cpf_mask_chars.sub('', s)
    return s


def _dv_maker(v):
    v %= 11
    if v >= 2:
        return 11 - v
    return 0


def validate_cpf(cpf):
    validate_digits_only(cpf)
    validate_has_exactly_len(cpf, CPF_LEN)
    cpf_without_dv = cpf[:-2]
    rev_digits = list(map(int, reversed(cpf_without_dv)))
    dv = sum(
        i * digit for i, digit in enumerate(rev_digits, start=2))
    dvs = [_dv_maker(dv)]
    rev_digits = chain(dvs, rev_digits)
    dv = sum(
        i * digit for i, digit in enumerate(rev_digits, start=2))
    dvs.append(_dv_maker(dv))
    if cpf[-2:] != ''.join(map(str, dvs)):
        raise ValidationError(_('Invalid CPF number.'))

    return cpf
