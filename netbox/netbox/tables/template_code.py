SEARCH_RESULT_ATTRS = """
{% for name, value in record.display_attrs.items %}
  {% with url=value.get_absolute_url %}
    <span class="badge bg-secondary" data-bs-toggle="tooltip" data-bs-placement="bottom" title="{{ name|bettertitle }}">
      {% if url %}<a href="{{ url }}">{% endif %}
      {{ value }}
      {% if url %}</a>{% endif %}
    </span>
  {% endwith %}
{% endfor %}
"""
