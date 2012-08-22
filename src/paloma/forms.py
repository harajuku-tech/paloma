# -*- coding: utf-8 -*-

from django import forms

from paloma.models import Group

class EnrollSignupForm(forms.Form):
    ''' Enroll Signup '''
    group = forms.ModelChoiceField(required = True, 
                    queryset = Group.objects.order_by('owner'))
