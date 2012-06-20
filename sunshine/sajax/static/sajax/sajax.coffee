
OK = 200

$.sajax = (fname, kwargs) ->
    [app, func] = fname.split '.'
    kwargs ?= {}

    response = $.ajax
        url: "/sajax/#{app}/#{func}/"
        type: 'POST'
        contentType: 'application/json'
        dataType: 'json'
        data: JSON.stringify kwargs
        processData: false
        async: false
        headers: {'X-Requested-With': 'XMLHttpRequest'}

    if response.status isnt OK
        throw new Error 'Error ' + response.status

    JSON.parse response.responseText
