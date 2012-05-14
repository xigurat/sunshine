
$ ->
    $('#logout').click (e) ->
        e.preventDefault()
        $.sajax 'ajaxauth.logout'
        if document.location.pathname isnt '/'
            document.location.pathname = '/'
        else
            document.location.reload()
