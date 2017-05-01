{{ name }}
===============================================================================
{{ short_desc }}

Attributes available for this component:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

======================================== =============== ========================================= =======================================
Name                                     Required        Type                                      Example
======================================== =============== ========================================= =======================================
{% for a in attrs %}
{% if a.has_docs %}{{ a.link|fill(40) }}{% else %}{{ a.name|fill(40) }}{%endif%} {{ a.required|fill(15) }} {{ ".. parsed-literal::"|fill(40) }}  .. parsed-literal::

{% for i in range(0,a.key_desc_len) %}
{% if i > a.key_example_len -1 %}
                                                          {{ a.key_desc[i]|fill(42) }}
{% else %}
                                                          {{ a.key_desc[i]|fill(42) }}{{ a.key_example[i] }}
{% endif %}
{% endfor %}
{% if a.name != attrs[-1].name %}
---------------------------------------- --------------- ----------------------------------------- ---------------------------------------
{% else %}
======================================== =============== ========================================= =======================================
{% endif %}
{% endfor %}

.. note::

  Problem how to read the table? Check out _Documentation

{{ doc }}

.. toctree::
  :maxdepth: 2

{% for a in attrs %}
{% if a.has_docs %}
  {{ a }}
{% endif %}
{% endfor %}
  


