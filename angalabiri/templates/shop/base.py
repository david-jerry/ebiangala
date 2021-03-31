{% extends "base.html" %}
{% load static i18n %}

{% block title %}
{{block.super}}
{% endblock title %}

{% block description %}
{% endblock description %}

{% block ogdesc %}
{% endblock ogdesc %}

{% block cano %}
{% endblock cano %}

{% block ogurl %}
{% endblock ogurl %}

{% block twitdesc %}
{% endblock twitdesc %}

{% block body-class %}
{% endblock body-class%}

{% block keywords %}
{% endblock keywords %}

{% block maincontent %}

<div class="clearfix" id="wrapper">
  {% include 'includes/shop/shopnav.html' %}

  {% if messages %}
  {% for message in messages %}
  <div class="alert {% if message.tags %}alert-{{ message.tags }}{% endif %}">{{ message }}<button type="button"
      class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>
  {% endfor %}
  {% endif %}

  {% block content %}
  {% endblock content %}
  {% include 'includes/pages/footer.html' %}
  {% include 'includes/pages/email.html' %}
</div> <!-- /wrapper -->
{% include 'includes/pages/totop.html' %}

{% block modal %}{% endblock modal %}

{% endblock maincontent %}

{% block inline_javascript %}
{% endblock inline_javascript %}


{% block javascript %}
{% include 'includes/shop/shopjs.html' %}
{% endblock javascript %}
