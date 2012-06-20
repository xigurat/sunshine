

window.{{ name_space }} ?= {}

{% for api in apis %}
class {{ name_space }}.{{ api.name }} extends Spine.Model
    @configure '{{ api.name }}', '{{ api.fields|join:"', '" }}'
    @extend Spine.Model.Ajax
    @url: '/api/{{ app_name }}/{{ api.name }}/'
{% endfor %}
