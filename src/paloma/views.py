# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
import sys

def u(view_name,args=[],kwargs={},absolute=lambda x: x ):
    return absolute( reverse (view_name, args=args,kwargs=kwargs ) )

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
