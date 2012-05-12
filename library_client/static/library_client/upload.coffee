
Book = Library.Book

class BookUploader extends Spine.Controller
    constructor: ->
        super
        @qq_uploader = new qq.FileUploader
            element: @el[0]
            action: Book.url
            allowedExtensions: ['pdf']
            debug: true
            onComplete: (id, filename, json_response) ->
                console.log  filename
                console.log  json_response

$ ->
    new BookUploader $ '#file-uploader'
