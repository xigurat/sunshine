(function() {
  $(window).scroll(function() {
    var $document, $window;
    $window = $(window);
    $document = $(document);
    if ($window.scrollTop() === $document.height() - $window.height()) {
      return $document.trigger('bottom_reached');
    }
  });
}).call(this);
