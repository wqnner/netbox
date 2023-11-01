SEARCH_RESULT_ATTRS = """
{% for name, value in record.display_attrs.items %}
  <span class="badge bg-secondary" data-bs-toggle="tooltip" data-bs-placement="bottom" title="{{ name|bettertitle }}">
    {{ value|linkify }}
  </span>
{% endfor %}
"""
