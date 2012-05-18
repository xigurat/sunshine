
window.Bootstrap ?= {}


class Bootstrap.Modal extends Spine.Controller

    elements:
        '[name]': 'fields'
        '[data-dismiss="modal"]': 'dismiss_buttons'

    events:
        'click .ok': 'on_ok'
        'click [data-dismiss="modal"]': 'on_dismiss'

    constructor: ->
        super
        @el.bind 'keypress': @on_keypress
        @el.bind 'hide': @on_hide
        @el.bind 'shown', @on_shown
        @el.bind 'hidden', @on_hidden
        @[field.name] = $(field) for field in @fields when field.name not of @

    on_keypress: (event) =>
        @on_ok() if (event.keyCode or event.which) == 13

    on_shown: =>
        @fields.first()?.focus()

    on_dismiss: =>
        @clear()

    on_hide: =>
        $(field).tooltip('hide') for field in @fields

    on_ok: =>
        null

    set_options: (options) ->
        @el.modal(options)

    hide: =>
        @el.modal 'hide'

    show: =>
        @el.modal 'show'

    clear: =>
        @fields.val ''


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

non_field_error_template = _.template "
    <div class='alert alert-error'>
        <a class='close' data-dismiss='alert'>×</a>
        <%= __all__.join('. ') %>
    </div>"

$.fn.showFormErrors = (errors, options) ->
    # Remove non field errors
    $('.alert', @).remove()

    # Remove field errors
    for element in $('[name]', @)
        $(element).tooltip('hide').data('tooltip', null).data('tooltip')
        $(element).parents('.control-group').removeClass('error')

    # Insert non field errors
    if errors.__all__?
        $('fieldset', @).prepend(non_field_error_template(errors))

    # Insert field errors
    for field_name, field_errors of errors
        field_errors = field_errors.join '. '
        $field = $ "[name='#{field_name}']", @

        # show errors
        current_options = $.extend(
            {title: field_errors, placement: 'right'},
            options)
        $field.tooltip(current_options).tooltip 'show'

        # set error class
        $field.parents('.control-group').addClass 'error'
x
