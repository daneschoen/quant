import os

from django import template


register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(value.file.name)


"""
And then in your template:

{% load filename %}

{# ... #}

{% for download in downloads %}
  <div class="download">
      <div class="title">{{download.file|filename}}</div>
  </div>
{% endfor %}

"""