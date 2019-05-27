{% assign responses = site.data.swagger[page.swaggerfile].[page.swaggerpath].[page.swaggerkey].[include.pagemethod].["responses"] %}
{% assign ref = $ref %}

{% assign _rcIdx = 0 %}
<table>
    <thead>
        <tr>
            <th>Code</th> 
            <th>Returns</th>
            <th>Type</th>
        </tr>
    </thead>
    <tbody>
        {% for code in responses %}
            {% assign rc = code[_rcIdx] %}
            <tr>
            <td>{{code[_rcIdx]}}</td>
            <td>{{responses[rc].["description"]}}</td>
            {% assign schema = responses[rc].["content"] %}
            {% if forloop.first %}              
                {% assign _type = schema["application/json"].["schema"].["type"] %}
                {% if _type == 'array' %}
                    {% assign _componentRef = schema["application/json"].["schema"].["items"].["$ref"] | remove_first:'#/components/schemas/' %}
                {% else %}
                {% assign _componentRef = schema["application/json"].["schema"].["$ref"] | remove_first:'#/components/schemas/' %}
                {% endif %}
            {% endif %}
            {% if schema["application/json"].["schema"].["type"] == 'array' %}
                {% assign componentRef = schema["application/json"].["schema"].["items"].["$ref"] | remove_first:'#/components/schemas/' %}
                {% assign linkText = componentRef | append: '[]' %}
            {% else %}
                {% assign componentRef = schema["application/json"].["schema"].["$ref"] | remove_first:'#/components/schemas/' %}
                {% assign linkText = componentRef  %}
            {% endif %}
            <td>
                <a href="userapi_components.html#{{ componentRef | downcase }}" >{{ linkText }}</a>
            </td>
            </tr>
            {% assign _rcIdx = (_rcIdx + 1) %}        
        {% endfor %}      
    </tbody>
</table>
{% include swagger_json/get_json_response_example.md componentName=_componentRef componentPath='components' componentType=_type %}
{{ _type["type"] }}
