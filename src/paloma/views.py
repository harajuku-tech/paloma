# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,redirect
from django import template

import sys

def u(view_name,args=[],kwargs={},absolute=lambda x: x ):
    return absolute( reverse (view_name, args=args,kwargs=kwargs ) )



def signin(request):
    """ Sign In """
    return render_to_response("paloma/signin.html",{},
                        context_instance=template.RequestContext(request),)

def signup(request):
    """ Sign Up """
    return render_to_response("paloma/signup.html",{},
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
