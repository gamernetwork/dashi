from django.conf import settings
from django.shortcuts import *
from django.template import RequestContext
from django.template import Template
from django.core import exceptions
import datetime
from django import http
from django.core import urlresolvers
from dashi import blocks
import sys

def render_blocks( request ):
    da_blocks = ""
    da_media = ""
    modules_used = set()
    for bl in blocks.blocks:
        da_blocks += bl.render( request )
        modules_used.add( bl.__class__ )
    for mod in iter( modules_used ):
        da_media += mod.render_support_media( request )
        
    return render_to_response( "dash.html", { "da_blocks" : da_blocks, "da_media" : da_media }, RequestContext(request) )
