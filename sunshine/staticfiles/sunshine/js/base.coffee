$ ->
    $('.search-query').typeahead
        sorter: ->
            return ['Arizona', 'Albania on cuba la  mas bonita y hermosa', 'Cuba la mas ']
            return $.fn.typeahead.Constructor.prototype.sorter.call(@, items)
