# -*- coding: utf-8 -*-

def enroll(request,command,secret):
    from django import template
    from django.http import HttpResponse
    return HttpResponse(
        template.Template("""
        <html><head><title>Paloma Enroll</title></head> <body> <h1> Paloma Enroll</h1>
            {{ command }} <br/>
            {{ secret  }} <br/>
        """
        ).render( template.RequestContext(request,
                {'command':command,'secret':secret}) )
    )
