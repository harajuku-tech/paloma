# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,redirect
from django import template
from django.views.generic.edit import FormView

from paloma.models import Group
from paloma.forms import SignUpMailForm
from paloma.actions import EnrollAction
import sys


class SignUpMailView(FormView):
    ''' Sign Up via Email
    '''
    template_name = "paloma/signup/mail.html" 
    form_class = SignUpMailForm 

    def get(self, *args, **kwargs):
        ''' GET '''
        if self.request.user.is_authenticated():
            #: TODO: to something ....
            pass

        return super(SignUpMailView, self).get(*args, **kwargs)

        
    def post(self, *args, **kwargs):
        ''' POST '''
        #: DEFAULT
        return super(SignUpMailView, self).post(*args, **kwargs)

    def get_initial(self):
        ''' initial '''
        return super(SignUpMailView, self).get_initial()

    def get_context_data(self, **kwargs):
        ''' Context , to the template'''
        ctx = kwargs
        ctx.update({
        })
        return ctx
    
    def form_valid(self, form):
        ''' When valid.
        ''' 
        e = EnrollAction.provide_signup( form.cleaned_data['group'] )
        email=e.signup_email()
        #: normatli redirect
        #: return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(email=email,form=form))

    def form_invalid(self, form):
        ''' When INvalid
        '''
        return super(SignUpMailView,self).form_invalid(form)


def u(view_name,args=[],kwargs={},absolute=lambda x: x ):
    return absolute( reverse (view_name, args=args,kwargs=kwargs ) )



def signin(request):
    """ Sign In """
    return render_to_response("paloma/signin.html",{},
                        context_instance=template.RequestContext(request),)

def signup_form(request):
    ''' signup via web form
    '''
    return render_to_response("paloma/signup/form.html",
                        {},
                        context_instance=template.RequestContext(request),)

def enroll(request,command,secret):
    from django import template
    from django.http import HttpResponse

    print sys.argv
    return HttpResponse(
        template.Template("""
        <html><head><title>Paloma Enroll</title></head> <body> <h1> Paloma Enroll</h1>
            {{ url     }} <br/>
            {{ aurl     }} <br/>
            {{ command }} <br/>
            {{ secret  }} <br/>
        """
        ).render( template.RequestContext(request,
                {'command':command,'secret':secret,
#                 'url' : request.build_absolute_uri('/o/my/god'),
#                 'url' : request.build_absolute_uri('/'),
                  'url' : u("paloma_enroll",kwargs={"command":"hoge","secret": "xxxx" },),
                  'aurl' : u("paloma_enroll",kwargs={"command":"hoge","secret": "xxxx" },absolute=request.build_absolute_uri),
                }) )
    )
