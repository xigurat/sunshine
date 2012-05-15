

class LoginController extends Bootstrap.Modal

    elements:
        '[name="username"]': 'username'
        '[name="password"]': 'password'

    constructor: ->
        super
        @login_error = new Bootstrap.ModalMessage
            el: $ '#login-error'
            parent: @

    on_ok: =>
        is_authenticated = $.sajax('ajaxauth.login'
            username: @username.val()
            password: @password.val()
        )
        if is_authenticated
            @hide()
            document.location.reload()
        else
            @login_error.show()


class SignupController extends Bootstrap.Modal

    elements:
        '[name="username"]': 'username'
        '[name="first_name"]': 'first_name'
        '[name="last_name"]': 'last_name'
        '[name="email"]': 'email'
        '[name="password1"]': 'password1'
        '[name="password2"]': 'password2'

    constructor: ->
        super
        @ajax_error = new Bootstrap.ModalMessage
            el: $ '#ajax-error'
            parent: @

        @signup_successful = new Bootstrap.ModalMessage
            el: $ '#signup-successful'
            on_show_call: @hide

    on_ok: =>
        try
            operation = $.sajax('ajaxauth.signup'
                username: @username.val()
                first_name: @first_name.val()
                last_name: @last_name.val()
                email: @email.val()
                password1: @password1.val()
                password2: @password2.val()
            )
        catch error
            @ajax_error.show()
            return

        if operation.is_success
            @log 'si'
            @signup_successful.show()
            @on_dismiss()
        else
            @el.showFormErrors operation.errors

$ ->
     window.login_controller = new LoginController el: $ '#login-dialog'
     window.signup_controller = new SignupController el: $ '#signup-dialog'
