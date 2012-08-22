# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,redirect
from django import template
from django.views.generic.edit import FormView

from paloma.models import Group
from paloma.forms import SignUpMailForm,SignUpWebForm,SignUpWebPreviewForm
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

class SignUpWebView(FormView):
    ''' Sign Up via Web 
    '''
    template_name = "paloma/signup/web/default.html" 
    form_class = SignUpWebForm 
    command = "default"

    def get(self,request, **kwargs):
        ''' GET '''
        if self.request.user.is_authenticated():
            #: TODO: to something ....
            pass

        return super(SignUpWebView, self).get(request, **kwargs)

        
    def post(self, request, **kwargs):
        ''' POST '''
        #: DEFAULT

        if request.POST.has_key('preview'):
            self.form_class = SignUpWebPreviewForm
            self.template_name = "paloma/signup/web/preview.html" 
            self.command="preview"
        elif request.POST.has_key('reedit'): 
            self.form_class = SignUpWebForm
            self.template_name = "paloma/signup/web/default.html" 
            self.command="reedit"
        elif request.POST.has_key('commit'):
            self.template_name = "paloma/signup/web/commit.html" 
            self.command="commit"
            
        return super(SignUpWebView, self).post(request, **kwargs)

    def get_initial(self):
        ''' initial '''
        return super(SignUpWebView, self).get_initial()

    def get_context_data(self, **kwargs):
        ''' Context , to the template'''
        ctx = kwargs
        ctx.update({
        })
        return ctx
    
    def form_valid(self, form):
        ''' When valid.
        ''' 
        if self.command == "commit":
            EnrollAction(self.request).enroll_by_web(
                form.cleaned_data['username']       ,
                form.cleaned_data['password']       ,
                form.cleaned_data['email']       ,
                form.cleaned_data['group']       ,
            )
            
        #:return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        ''' When INvalid
        '''
        form = self.get_form( SignUpWebForm )   #: Re Edit anyway
        self.template_name = "paloma/signup/web/default.html" 

        return super(SignUpWebView,self).form_invalid(form)


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
                  'aurl' : u("paloma_enroll",kwargs={"command":"hoge","secret": "xxxx" },
                        absolute=request.build_absolute_uri),
                }) )
    )
