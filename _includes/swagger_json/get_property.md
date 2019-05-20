{% assign _path = site.data.swagger[page.swaggerfile] %}
{% assign _key = page.swaggerkey %}
{% assign _method = page.method %}
{% assign _prop = include.attribute %}
{{ _path.paths[_key].[_method].[_prop] }}



