# -*- coding: utf-8 -*-

def enroll(request,command,secret):
    from django import template
    from django.http import HttpResponse

    print type(request)
    return HttpResponse(
        template.Template("""
        <html><head><title>Paloma Enroll</title></head> <body> <h1> Paloma Enroll</h1>
            {{ url     }} <br/>
            {{ command }} <br/>
            {{ secret  }} <br/>
        """
        ).render( template.RequestContext(request,
                {'command':command,'secret':secret,
                 'url' : request.build_absolute_uri('/o/my/god'),
                }) )
    )
