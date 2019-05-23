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
            {% if schema["application/json"].["schema"].["type"]  %}
                {% assign componentRef = schema["application/json"].["schema"].["items"].["$ref"] | remove_first:'#/components/schemas/' %}
            {% else %}
                {% assign componentRef = schema["application/json"].["schema"].["$ref"] | remove_first:'#/components/schemas/' %}
            {% endif %}
            <td>
                <a href="userapi_components.html#{{ componentRef | downcase }}" >{{ componentRef }}</a>
            </td>
            </tr>
            {% assign _rcIdx = _rcIdx + 1 %}        
        {% endfor %}      
    </tbody>
</table>
