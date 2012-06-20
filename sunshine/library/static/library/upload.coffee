

class Library.BookUploader extends Spine.Controller

    constructor: ->
        super
        @qq_uploader = new qq.FileUploader
            element: @el[0]
            action: Library.Book.url
            allowedExtensions: ['pdf']
            maxConnections: 3
            debug: true

            template: '
                <div class="qq-uploader">
                    <div class="qq-upload-drop-area well centered">
                        Drop files here to upload
                    </div>
                    <div class="row">
                        <div class="qq-upload-button btn btn-primary pull-right">
                            <i class="icon-upload icon-white"></i>
                            Upload a file
                        </div>
                    </div>
                    <ul class="qq-upload-list" style="list-style:none; margin: 10px 0;"></ul>
                </div>
            '

            fileTemplate: '<li class="row">
                <span class="span3 qq-upload-file"></span>
                <span class="row">
                    <span class=" qq-upload-spinner"></span>
                    <span class="span3 qq-upload-size"></span>
                    <span class="qq-upload-failed-text"></span>
                </span>

                <span class="row-fluid qq-upload-spinner">
                    <div class="span1">&nbsp;</div>
                    <div class="span9">
                        <div class="progress">
                            <div class="bar"></div>
                        </div>
                    </div>
                    <span class="span2">
                        <a class="btn btn-mini btn-danger qq-upload-cancel" href="#">Cancel</a>
                    </span>
                </span>

                </li>
            '

            onProgress:  (id, file_name, loaded, total) ->
                percent = loaded / total * 100
                $bar = $('.bar', $('.qq-upload-list li')[id])
                $bar.css 'width', "#{percent}%"

            onComplete: (id, file_name, response) ->
                $($('.qq-upload-list li')[id]).slideUp()
                Library.Book.fetch $.query id: response.id

$ ->
    Library.book_uploader = new Library.BookUploader el: $ '#file-uploader'
