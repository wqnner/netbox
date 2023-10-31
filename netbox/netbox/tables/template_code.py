SEARCH_RESULT_ATTRS = """
{% for name, value in record.display_attrs.items %}
  {% with url=value.get_absolute_url %}
    <span class="badge bg-secondary">
      {% if url %}<a href="{{ url }}">{% endif %}
      {{ name|bettertitle }}: {{ value }}
      {% if url %}</a>{% endif %}
    </span>
  {% endwith %}
{% endfor %}
"""
