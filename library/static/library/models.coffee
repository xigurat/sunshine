

window.Library ?= {}


class Library.Author extends Spine.Model
    @configure 'Author', 'id', 'name'
    @extend Spine.Model.Ajax
    @url: '/api/library/Author/'

class Library.Book extends Spine.Model
    @configure 'Book', 'title', 'language', 'id', 'summary', 'n_pages', 'get_absolute_url', 'short_url', 'date', 'uploader_username', 'thumbnail_url', 'file', 'get_edition_url', 'later_editions_ids', 'previous_editions_ids', 'success', 'source', 'relation', 'format', 'success'
    @extend Spine.Model.Ajax
    @url: '/api/library/Book/'

