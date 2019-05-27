{%- assign _jsonName = include.componentName -%}
{%- assign _jsonPath = include.componentPath -%}
{%- assign _jsonType = include.componentType -%}
{%- assign schemas = site.data.swagger[page.swaggerfile].[_jsonPath].["schemas"] -%}
{%- assign _hIdx = 0 -%}
{%- assign _typeJson = schemas[_jsonName]  -%}
{%- if _typeJson -%}
    {% if _jsonType == "array" %} 
            [{ 
    {% else %} 
            { 
    {% endif %}
    {%- for _props in _typeJson["properties"] -%}
        {%- assign _name = _props[_hIdx] -%}
        {% if forloop.first %}           "{{- _props[_hIdx] -}}"{% else %}
                "{{- _props[_hIdx] -}}"
        {%- endif -%}
                    : "{{- _typeJson["properties"].[_name].["type"] -}}"
        {%- if _typeJson["properties"].[_name].["description"] != null and _typeJson["properties"].[_name].["description"] != "" -%}
            // {{ _typeJson["properties"].[_name].["description"] }}             
            {%- unless forloop.last -%},{%- endunless -%}
        {%- else -%}
            {%- unless forloop.last -%},{%- endunless -%}    
        {%- endif -%}
        {%- assign _hIdx = _hIdx + 1 -%}
    {%- endfor -%}
    {% if _jsonType == "array" %}
        }]
    {% else %}
            }
    {%- endif -%}
{%- endif -%}