{% assign parameters = site.data.swagger[page.swaggerfile].[page.swaggerpath].[page.swaggerkey].[include.pagemethod].["parameters"] %}
{% assign ref = $ref %}

{% assign _rcIdx = 0 %}
<table>
    <thead>
        <tr>
            <th>Name</th> 
            <th>In</th>
            <th>Description</th>
            <th>Required</th>
            <th>Type</th>
        </tr>
    </thead>
    <tbody>
        {% for parameter in parameters %}
            {% assign rc = parameter[_rcIdx] %}
            <tr>
            <td>{{parameter["name"]}}</td>
            <td>{{parameter["in"]}}</td>
            <td>{{parameter["description"]}}</td>
            <td>{{parameter["required"]}}</td>
            <td>{{parameter["schema"]["type"]}}</td>           
            </tr>
            {% assign _rcIdx = _rcIdx + 1 %}        
        {% endfor %}      
    </tbody>
</table>