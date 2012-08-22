# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import re

from paloma.models import Group,Mailbox

alphanum_re = re.compile(r"^\w+$")

class SignUpMailForm(forms.Form):
    ''' Enroll Signup '''
    group = forms.ModelChoiceField(required = True, 
                    queryset = Group.objects.order_by('owner'))

class SignUpWebPreviewForm(forms.Form):
    
    username = forms.CharField(
        label=_("User login name"),
        max_length=30,
        widget=forms.HiddenInput(),
        required=True
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.HiddenInput(),
    )
    password_confirm = forms.CharField(
        label=_("Password (again)"),
        widget=forms.HiddenInput(),
    )
    email = forms.EmailField(
        widget=forms.HiddenInput(),
        required=True)

    group = forms.ModelChoiceField(required = True, 
                widget=forms.HiddenInput(),
                queryset = Group.objects.order_by('owner'))

    def clean_username(self):
        ''' check "username" '''
        if not alphanum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_("Usernames can only contain letters, numbers and underscores."))
        qs = User.objects.filter(username__iexact=self.cleaned_data["username"])
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))
    
    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = Mailbox.objects.filter(address__iexact=value)
        if not qs.exists() : 
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))
    
    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("Must be same password."))
        return self.cleaned_data

class SignUpWebForm(forms.Form):
    
    username = forms.CharField(
        label=_("User login name"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )
    email = forms.EmailField(widget=forms.TextInput(), required=True)

    group = forms.ModelChoiceField(required = True, 
                    queryset = Group.objects.order_by('owner'))

    def clean_username(self):
        ''' check "username" '''
        if not alphanum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_("Usernames can only contain letters, numbers and underscores."))
        qs = User.objects.filter(username__iexact=self.cleaned_data["username"])
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))
    
    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = Mailbox.objects.filter(address__iexact=value)
        if not qs.exists() : 
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))
    
    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("Must be same password."))
        return self.cleaned_data
