from django.conf import settings
from django.shortcuts import *
from django.template import RequestContext
from dashi import blocks
from django.utils import simplejson
from django.http import HttpResponse


def render_blocks(request):
    da_blocks = ""
    da_media = ""
    modules_used = set()
    for bl in blocks.blocks:
        da_blocks += bl.render(request)
        modules_used.add(bl.__class__)
    for mod in iter(modules_used):
        da_media += mod.render_support_media(request)

    style_override = settings.DASHBOARD_STYLE_OVERRIDE

    return render_to_response("dash.html", {"da_blocks": da_blocks, "da_media": da_media, "style_override": style_override, "settings": settings}, RequestContext(request))


def ajax_update_block(request, block_id):
    for bl in blocks.blocks:
        if str(bl.block_id) == str(block_id):
            s = simplejson.dumps(bl.update(request))
            return HttpResponse(s)
    return HttpResponse("")
