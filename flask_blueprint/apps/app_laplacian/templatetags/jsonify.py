

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.template import Library
import json

register = Library()

def jsonify(object):
    if isinstance(object, QuerySet):
        #return serialize('json', object)
        return mark_safe(serialize('json', object))
    #return json.dumps(object)
    return mark_safe(json.dumps(object))

register.filter('jsonify', jsonify)
jsonify.is_safe = True


"""
Usage:

{% load json_filters %}

{% block content %} &lt;script type="text/javascript"&gt;<![CDATA[ var items = {{ items|jsonify }}; ]]>&lt;/script&gt; {% endblock %}



import json
from django.core.serializers.json import DjangoJSONEncoder

prices = Price.objects.filter(product=product).values_list('price', 'valid_from')

prices_json = json.dumps(list(prices), cls=DjangoJSONEncoder)
"""