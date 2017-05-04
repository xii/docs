{{ name }}
===============================================================================
{% if help %}
{{ help }}
{% endif %}

::

{% for line in commandline %}
  {{ line }}
{% endfor %}

{{ description }}
