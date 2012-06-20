
Book = Library.Book

class Library.BookList extends Spine.Controller
    elements:
        'li': 'list_items'

    constructor: ->
        super
        @items = []
        Book.bind 'refresh', @render_all
        Book.fetch()

    render_all: (books) =>
        @render_one book for book in books
        @append $.render book_list_blank_state unless books.length

    add_item: (item) ->
        i = _.sortedIndex @items, item, (x) ->
            -Date.parse(x.book.upload_datetime)
        @items = @items[..i-1].concat [item], @items[i..]
        i

    render_one: (book) =>
        item = new Library.BookItem book: book
        index = @add_item item
        element = item.render()
        if index is 0
            @prepend element
        else if index == @list_items.length
            @append element
        else
            $(@list_items[index]).before element
            @refreshElements()

        element.slideDown()


class Library.BookItem extends Spine.Controller
    events:
        'click .edit': 'on_edit'
        'click .read': 'on_read'
        'click .delete': 'on_delete'

    constructor: ->
        super
        @book.bind 'update', @render
        @book.bind 'destroy', @el.remove

    render: =>
        @replace $.render book_template, @book
        @el


$ ->
    book_template = $.jqotec '#book_template'
    book_list_blank_state = $.jqotec '#book_list_blank_state'
    Library.book_list = new Library.BookList el: $ '.book-list'
