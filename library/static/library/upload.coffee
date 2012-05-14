

class Library.BookUploader extends Spine.Controller

    constructor: ->
        super
        @qq_uploader = new qq.FileUploader
            element: @el[0]
            action: Library.Book.url
            allowedExtensions: ['pdf']
            debug: true

            template: '
                <div class="qq-uploader">
                    <div class="qq-upload-drop-area well">
                        Drop files here to upload
                    </div>
                    <div class="row">
                        <div class="qq-upload-button btn btn-primary pull-right">
                            Upload a file
                        </div>
                    </div>
                    <ul class="qq-upload-list"></ul>
                </div>
            '

            fileTemplate: '<li>
                <span class="qq-upload-file"></span>
                <span class="qq-upload-spinner"></span>
                <span class="qq-upload-size"></span>
                <div class="qq-upload-spinner progress">
                    <div class="bar"></div>
                </div>
                <a class="qq-upload-cancel" href="#">Cancel</a>
                <span class="qq-upload-failed-text">Failed</span>
                </li>
            '

            onProgress: (id, fileName, loaded, total) ->
                percent = loaded / total * 100
                $bar = $('.bar', $('.qq-upload-list li')[id])
                $bar.css 'width', "#{percent}%"


$ ->
    Library.book_uploader = new Library.BookUploader el: $ '#file-uploader'
