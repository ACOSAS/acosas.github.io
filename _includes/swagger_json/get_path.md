<div>
{% assign _methods = site.data.swagger[page.swaggerfile][page.swaggerpath][page.swaggerkey] | json %}
{% assign _midx = 0 %}

{% for _method in _methods %}
   <h2>{{ _method[_midx] | upcase }} {{ page.swaggerkey | downcase }}</h2>
   {% assign _methodname = _method[_midx] %}
    {% if _methods[_methodname]["summary"] != "" %} 
        <p>{{_methods[_methodname]["summary"]}}</p>
        {% include swagger_json/overlay_slot.md slot="after_summary" %}
    {% endif %}
    {% if _methods[_methodname]["description"] %} 
        <h4>Description</h4>
        <p>{{_methods[_methodname]["description"]}}</p>
        {% include swagger_json/overlay_slot.md slot="after_description" %}
    {% endif %}
    {% if _methods[_methodname]["parameters"] %}
        <h4>Parameters</h4>
         {% include swagger_json/get_parameters.md pagemethod=_methodname %}
         {% include swagger_json/overlay_slot.md slot="after_parameters" %}
    {% endif %}
    {% if _methods[_methodname]["requestBody"]  %}
        <h4>Request body</h4>
        {%- assign _requestBodyName =  _methods[_methodname]["requestBody"]["content"]["application/json"]["schema"]["$ref"] | remove_first:'#/components/schemas/' -%}
        {%- include swagger_json/get_model_highlight.md componentName=_requestBodyName componentPath=page.swagger_components componentType='object' -%}
    {% endif %}
        {% include swagger_json/overlay_slot.md slot="after_request_body" %}
         <h4>Responses</h4>       
        {% include swagger_json/get_responses.md pagemethod=_methodname %}
        {% include swagger_json/overlay_slot.md slot="after_responses" %}
{% endfor %}

</div>
