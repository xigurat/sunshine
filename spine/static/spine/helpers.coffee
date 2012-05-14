
$.query = (query_data) ->
    data: JSON.stringify(query_data or {})

$.getCookies = () ->
    cookies = {}
    for cookie in document.cookie.split('; ')
        [attr_name, value] = cookie.split('=')
        cookies[attr_name] = value
    cookies

$.render = (template, data) ->
    jQuery jQuery.jqote template, data

$.setChecked = (checkbox, value) ->
    if value
        checkbox.attr 'checked', 'checked'
    else
        checkbox.removeAttr 'checked'


isNumberKey = (event) ->
    charCode = event.which or event.keyCode
    if charCode > 31 and (charCode < 48 or charCode > 57)
        return false;
    return true;


isMoneyKey = (event) ->
    charCode = event.which or event.keyCode
    if charCode > 31 and (charCode < 48 or charCode > 57) and charCode != 46
        return false;
    return true;


csrfToken = $.getCookies()['csrftoken']
$(document).ajaxSend (e, xhr, settings) =>
    xhr.setRequestHeader 'X-CSRFToken', csrfToken


$ ->
    $(number).live('keypress', isNumberKey) for number in [
        'input.number', 'input[name="phone"]', 'input[name="cellphone"]',
        'input[name="social_security_number"]', 'input.vIntegerField',
    ]

    $(float).live('keypress', isMoneyKey) for float in [
        'input[name="salary"]', 'input.money',
    ]
