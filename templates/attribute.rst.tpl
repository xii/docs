{{ name }}
===============================================================================

Definition:
^^^^^^^^^^^
.. parsed-literal::
  {{ name }}: {% for i in range(0,key_desc_len) %}{{ key_desc[i] }}{% endfor %}

{% if example %}
Example:

.. parsed-literal::

  {{ example }}

{% endif %}

Documentation:
^^^^^^^^^^^^^^

{{ docs }}
