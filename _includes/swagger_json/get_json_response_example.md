{% assign _responseName = include.componentName %}
{% assign _responsePath = include.componentPath %}
{% assign _responseType = include.componentType %}
{% assign schemas = site.data.swagger[page.swaggerfile].[_responsePath].["schemas"] %}
{% assign _cIdx = 0 %}

{% assign _responseJsonType = schemas[_responseName]  %}
{% if _responseJsonType %}
<h5>Response Example</h5>
{%- endif -%}
{%- include swagger_json/get_model_highlight.md componentName=_responseName componentPath='components' componentType=_responseType -%}