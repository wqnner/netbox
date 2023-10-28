SEARCH_RESULT_ATTRS = """
{% for name, value in record.display_attrs.items %}
  <span class="badge bg-secondary">{{ name|bettertitle }}: {{ value }}</span>
{% endfor %}
"""
