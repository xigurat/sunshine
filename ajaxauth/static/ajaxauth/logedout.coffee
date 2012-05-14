

class LoginController extends Boostrap.Modal
    events:
        'click .login': 'on_login'

    elements:
        '[name="username"]': 'username'
        '[name="password"]': 'password'

    constructor: ->
        super
        @login_error = $ '#login-error'
        @login_error.bind 'hidden', @show

    on_login: =>
        @hide()
        is_authenticated = $.sajax('ajaxauth.login'
            username: @username.val()
            password: @password.val()
        )
        if is_authenticated
            document.location.reload()
        else
            @login_error.modal 'show'


class SignupController extends Boostrap.Modal


$ ->
     window.login_controller = new LoginController el: $ '#login-dialog'
