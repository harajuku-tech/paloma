# -*- coding: utf-8 -*-

from django import forms

from paloma.models import Group

class SignUpMailForm(forms.Form):
    ''' Enroll Signup '''
    group = forms.ModelChoiceField(required = True, 
                    queryset = Group.objects.order_by('owner'))
