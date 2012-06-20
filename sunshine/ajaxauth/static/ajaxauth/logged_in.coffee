
class ChangePasswordController extends Bootstrap.Modal
    constructor: ->
        super
        @password_changed_ok = new Bootstrap.ModalMessage
            el: $ '#password-changed-successfully'
            on_show_call: @hide

    on_ok: =>
        operation = $.sajax('ajaxauth.change_password'
            old_password: @old_password.val()
            new_password1: @new_password1.val()
            new_password2: @new_password2.val()
        )
        if operation.is_success
            @password_changed_ok.show()
            @on_dismiss()
        else
            @el.showFormErrors operation.errors


$ ->
    window.change_password_controller = new ChangePasswordController
        el: $ '#change-password-dialog'

    $('#logout').click (e) ->
        e.preventDefault()
        $.sajax 'ajaxauth.logout'
        document.location.reload()
