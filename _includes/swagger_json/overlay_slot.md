{% if site.data.overlays and site.data.overlays.entries %}
{% for _overlay_entry in site.data.overlays.entries %}
{% if _overlay_entry.swaggerfile == page.swaggerfile and _overlay_entry.path == page.swaggerkey and _overlay_entry.slot == include.slot %}
<div class="openapi-overlay" data-slot="{{ include.slot }}">
{{ _overlay_entry.markdown | markdownify }}
</div>
{% endif %}
{% endfor %}
{% endif %}
