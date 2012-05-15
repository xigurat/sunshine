
window.Bootstrap ?= {}


class Bootstrap.Modal extends Spine.Controller

    events:
        'click .ok': 'on_ok'
        'click [data-dismiss="modal"]': 'on_dismiss'

    constructor: ->
        super
        @inputs = $ 'input', @el
        @dismiss_buttons = $ '[data-dismiss="modal"]', @el
        @el.bind 'keypress': @on_keypress
        @el.bind 'shown', @on_shown
        @el.bind 'hidden', @on_hidden

    on_keypress: (event) =>
        @on_ok() if (event.keyCode or event.which) == 13

    on_shown: =>
        @inputs.first()?.focus()

    on_dismiss: =>
        @clear()

    on_ok: =>
        null

    set_options: (options) ->
        @el.modal(options)

    hide: =>
        @el.modal 'hide'

    show: =>
        @el.modal 'show'

    clear: =>
        @inputs.val ''


class Bootstrap.ModalMessage extends Bootstrap.Modal
    constructor: ->
        super
        @el.bind 'show', @on_show

    on_show: =>
        @on_show_call?()
        @parent?.hide()

    on_hidden: =>
        @on_hidden_call?()
        @parent?.show()


# jQuery plugins


$.fn.showFormErrors = (errors) ->
    for element in $('[name]')
        $(element).tooltip('hide').data('tooltip', null).data('tooltip')
        $(element).parents('.control-group').removeClass('error')

    for field_name, field_errors of errors
        field_errors = field_errors.join '\n'
        $field = $ "[name='#{field_name}']", @

        #show errors
        $field.tooltip(title: field_errors).tooltip 'show'

        #set error class
        $field.parents('.control-group').addClass 'error'

        #hide when modal is hidden
        $field.parents('.modal').bind 'hide', ->
            $field.tooltip 'hide'
