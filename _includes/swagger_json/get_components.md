{% if page.swaggerkey == "components" %}
{% assign schemas = site.data.swagger[page.swaggerfile].[page.swaggerkey].["schemas"] %}
{% else %}
{% assign schemas = site.data.swagger[page.swaggerfile].[page.swaggerkey] %}
{% endif %}
{% assign _cIdx = 0 %}

<div>
{% for component in schemas %}
    {% assign componentName = component[_cIdx] %}
    <h2>{{componentName}}</h2>
    <p>Type: {{schemas[componentName].["type"]}}</p>
    <h3>Properties</h3>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Format</th>
            </tr>
        </thead>
        <tbody>
            {% assign componentProp = schemas[componentName].["properties"] %}
                {% assign _pIdx = 0 %}
                {% for prop in componentProp %}                                        
                    {% assign cp = prop[_pIdx] %}
                    <tr>
                        <td>{{cp}}</td>
                        <td>{{componentProp[cp].["type"]}}</td>
                        <td>{{componentProp[cp].["format"]}}</td>
                    </tr>
                    {% assign _pIdx = _pIdx + 1  %} 
                {% endfor %}
        </tbody>
    </table>
    {% assign _cIdx = _cIdx + 1 %}
{% endfor %}
</div>