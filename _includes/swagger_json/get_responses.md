{% assign responses = site.data.swagger[page.swaggerfile].[page.swaggerpath].[page.swaggerkey].[include.pagemethod].["responses"] %}
{% assign ref = $ref %}
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
            {% assign rc = code[forloop.index0] %}
            <td>{{code[forloop.index0]}}</td>
            <td>{{responses[rc].["description"]}}</td>
            {% assign schema = responses[rc].["content"] %}
            {% assign componentRef = schema["application/json"].["schema"].["$ref"] | remove_first:'#/components/schemas/' %}
            <td>
                <a href="userapi_components.html#{{ componentRef | downcase }}" >{{ componentRef }}</a>
            </td>        
        {% endfor %}      
    </tbody>
</table>
