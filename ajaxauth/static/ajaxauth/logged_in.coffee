
$ ->
    $('#logout').click (e) ->
        e.preventDefault()
        $.sajax 'ajaxauth.logout'
        document.location.reload()
