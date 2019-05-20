<div>
{% assign _methods = site.data.swagger[page.swaggerfile][page.swaggerpath][page.swaggerkey] | json %}
{% assign _midx = 0 %}

{% for _method in _methods %}
   <h2>{{ _method[_midx] | upcase }} {{ page.swaggerkey | downcase }}</h2>
   {% assign _methodname = _method[_midx] %}
    {% if _methods[_methodname]["summary"] != "" %} 
        <p>{{_methods[_methodname]["summary"]}}</p>       
    {% endif %}
         <h4>Responses</h4>       
        {% include swagger_json/get_responses.md pagemethod=_methodname %}
{% endfor %}

</div>