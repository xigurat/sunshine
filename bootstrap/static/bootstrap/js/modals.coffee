
window.Boostrap ?= {}


class  Boostrap.Modal extends Spine.Controller

    constructor: ->
        super
        @inputs = $ 'input', @el
        @el.bind 'shown', @on_shown
        @el.bind 'hidden', @on_hidden

    on_shown: =>
        if @inputs.length
            $(@inputs[0]).focus()

    on_hidden: =>
        @clear()

    hide: =>
        @el.modal 'hide'

    show: =>
        @el.modal 'show'

    clear: =>
        @inputs.val ''
