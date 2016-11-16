#from dajax.core import Dajax
from django.utils import simplejson
from dajaxice.core import dajaxice_functions
from dajaxice.decorators import dajaxice_register
from dashi import blocks

#    buttonHTML = render_to_string(
#        'incart.html',
#        {},
#        context_instance = RequestContext( request )
#    )
#    return simplejson.dumps( { 'cartHTML' : rendered, 'buttonHTML' : buttonHTML, 'cartCount' : request.cart.length() } )
#dajaxice_functions.register(cart_add)

@dajaxice_register( method="GET" )
def update_block( request, block_id ):
    for bl in blocks.blocks:
        if str( bl.block_id ) == str( block_id ):
            s = simplejson.dumps( bl.update( request ) )
            return s
    return ""
