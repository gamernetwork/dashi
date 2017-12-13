from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dashi import blocks

@dajaxice_register( method="GET" )
def update_block( request, block_id ):
    for bl in blocks.blocks:
        if str( bl.block_id ) == str( block_id ):
            s = simplejson.dumps( bl.update( request ) )
            return s
    return ""
