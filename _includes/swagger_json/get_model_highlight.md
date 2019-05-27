{%- assign _highlightName = include.componentName -%}
{%- assign _highlighPath = include.componentPath -%}
{%- assign _highlightType = include.componentType -%}
{%- assign schemas = site.data.swagger[page.swaggerfile].[_highlighPath].["schemas"] -%}
{%- assign _mIdx = 0 -%}
{%- assign _ref = "$ref" -%}
{%- assign _typeHightlight = schemas[_highlightName]  -%}
{%- if _typeHightlight -%}
{%- highlight json -%}
{%- if _highlightType == "array" -%}
[{ 
{%- else -%} 
{ 
{% endif %}
{%- for _props in _typeHightlight["properties"] -%}
    {%- assign _name = _props[_mIdx] -%}
    {% if forloop.first %}        
        "{{- _props[_mIdx] -}}"
    {%- else -%}
        "{{- _props[_mIdx] -}}"
    {%- endif -%}
     : 
    {%- if _typeHightlight["properties"].[_name].[_ref] -%}
        {%- assign _subType1 = _typeHightlight["properties"].[_name].["type"] -%}
        {%- assign _subName1 = _typeHightlight["properties"].[_name].[_ref] | remove_first:'#/components/schemas/' -%}
        {%- include swagger_json/get_model_json.md componentName=_subName1 componentPath=_highlighPath componentType=_subType1 -%}
    {%- elsif _typeHightlight["properties"].[_name].["type"] == 'array' -%}
        {%- assign _subType2 = _typeHightlight["properties"].[_name].["type"] -%}             
        {%- assign _subName2 = _typeHightlight["properties"].[_name].["items"].[_ref] | remove_first:'#/components/schemas/' -%}
        {{- _subType -}}
        {%- include swagger_json/get_model_json.md componentName=_subName2 componentPath=_highlighPath componentType=_subType2 -%}
    {%- else -%}
        "{{- _typeHightlight["properties"].[_name].["type"] -}}"       
    {%- endif -%}   
    {% if _typeHightlight["properties"].[_name].["description"] != null and _typeHightlight["properties"].[_name].["description"] != "" %} // {{- _typeHightlight["properties"].[_name].["description"] -}}
        {% unless forloop.last %},
        {% endunless %}
    {%- else -%}             
        {% unless forloop.last %},
        {% endunless %}
    {%- endif -%}
    {%- assign _mIdx = (_mIdx + 1) -%}
{%- endfor -%}
{% if _highlightType == "array" %}
}]
{% else %}
}
{% endif %}
{%- endhighlight -%}
{%- endif -%}