// Generated by CoffeeScript 1.3.1
(function() {
  var Book, BookUploader,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  Book = Library.Book;

  BookUploader = (function(_super) {

    __extends(BookUploader, _super);

    BookUploader.name = 'BookUploader';

    function BookUploader() {
      BookUploader.__super__.constructor.apply(this, arguments);
      this.qq_uploader = new qq.FileUploader({
        element: this.el[0],
        action: Book.url,
        allowedExtensions: ['pdf'],
        debug: true,
        onComplete: function(id, filename, json_response) {
          console.log(filename);
          return console.log(json_response);
        }
      });
    }

    return BookUploader;

  })(Spine.Controller);

  $(function() {
    return new BookUploader($('#file-uploader'));
  });

}).call(this);