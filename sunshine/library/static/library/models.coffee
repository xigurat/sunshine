

window.Library ?= {}


class Library.Author extends Spine.Model
    @configure 'Author', 'id', 'name'
    @extend Spine.Model.Ajax
    @url: '/api/library/Author/'

class Library.Book extends Spine.Model
    @configure 'Book', 'id', 'title', 'title', 'n_pages', 'date', 'authors', 'summary', 'date', 'uploader_username', 'upload_datetime', 'file', 'thumbnail_url', 'short_url', 'success'
    @extend Spine.Model.Ajax
    @url: '/api/library/Book/'

