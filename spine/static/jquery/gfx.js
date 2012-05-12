(function() {
  var $, chrome11, chromeMatch, chromeRegex, close, defaults, isOpen, n, overlayStyles, panelCSS, prefix, sides, transformTypes, vendor, vendorNames;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; }, __indexOf = Array.prototype.indexOf || function(item) {
    for (var i = 0, l = this.length; i < l; i++) {
      if (this[i] === item) return i;
    }
    return -1;
  };
  $ = this.jQuery;
  if (!$) {
    throw 'jQuery required';
  }
  defaults = {
    duration: 400,
    queue: true,
    easing: ''
  };
  vendor = $.browser.mozilla ? 'moz' : void 0;
  vendor || (vendor = 'webkit');
  prefix = "-" + vendor + "-";
  vendorNames = n = {
    transition: "" + prefix + "transition",
    transform: "" + prefix + "transform",
    transitionEnd: "" + vendor + "TransitionEnd"
  };
  transformTypes = ['scale', 'scaleX', 'scaleY', 'scale3d', 'rotate', 'rotateX', 'rotateY', 'rotateZ', 'rotate3d', 'translate', 'translateX', 'translateY', 'translateZ', 'translate3d', 'skew', 'skewX', 'skewY', 'matrix', 'matrix3d', 'perspective'];
  $.fn.queueNext = function(callback, type) {
    type || (type = "fx");
    return this.queue(function() {
      callback.apply(this, arguments);
      return setTimeout(__bind(function() {
        return jQuery.dequeue(this, type);
      }, this));
    });
  };
  $.fn.emulateTransitionEnd = function(duration) {
    var callback, called;
    called = false;
    $(this).one(n.transitionEnd, function() {
      return called = true;
    });
    callback = __bind(function() {
      if (!called) {
        return $(this).trigger(n.transitionEnd);
      }
    }, this);
    return setTimeout(callback, duration);
  };
  $.fn.transform = function(properties) {
    var key, transforms, value;
    transforms = [];
    for (key in properties) {
      value = properties[key];
      if (__indexOf.call(transformTypes, key) >= 0) {
        transforms.push("" + key + "(" + value + ")");
        delete properties[key];
      }
    }
    if (transforms.length) {
      properties[n.transform] = transforms.join(' ');
    }
    return $(this).css(properties);
  };
  $.fn.gfx = function(properties, options) {
    var callback, opts;
    opts = $.extend({}, defaults, options);
    properties[n.transition] = "all " + opts.duration + "ms " + opts.easing;
    callback = function() {
      var _ref;
      $(this).css(n.transition, '');
      if ((_ref = opts.complete) != null) {
        _ref.apply(this, arguments);
      }
      return $(this).dequeue();
    };
    return this[opts.queue === false ? 'each' : 'queue'](function() {
      $(this).one(n.transitionEnd, callback);
      $(this).transform(properties);
      return $(this).emulateTransitionEnd(opts.duration + 50);
    });
  };
  $.fn.gfxPopIn = function(options) {
    var _ref;
    if (options == null) {
      options = {};
    }
        if ((_ref = options.scale) != null) {
      _ref;
    } else {
      options.scale = '.2';
    };
    $(this).queueNext(function() {
      return $(this).transform({
        '-webkit-transform-origin': '50% 50%',
        '-moz-transform-origin': '50% 50%',
        scale: options.scale,
        opacity: '0',
        display: 'block'
      });
    });
    return $(this).gfx({
      scale: '1',
      opacity: '1'
    }, options);
  };
  $.fn.gfxPopOut = function(options) {
    $(this).queueNext(function() {
      return $(this).transform({
        '-webkit-transform-origin': '50% 50%',
        '-moz-transform-origin': '50% 50%',
        scale: '1',
        opacity: '1'
      });
    });
    $(this).gfx({
      scale: '.2',
      opacity: '0'
    }, options);
    return $(this).queueNext(function() {
      return $(this).transform({
        display: 'none',
        opacity: '1',
        scale: '1'
      });
    });
  };
  $.fn.gfxFadeIn = function(options) {
    var _ref;
    if (options == null) {
      options = {};
    }
        if ((_ref = options.duration) != null) {
      _ref;
    } else {
      options.duration = 1000;
    };
    $(this).queueNext(function() {
      return $(this).css({
        display: 'block',
        opacity: '0'
      });
    });
    return $(this).gfx({
      opacity: 1
    }, options);
  };
  $.fn.gfxFadeOut = function(options) {
    if (options == null) {
      options = {};
    }
    $(this).queueNext(function() {
      return $(this).css({
        opacity: 1
      });
    });
    $(this).gfx({
      opacity: 0
    }, options);
    return $(this).queueNext(function() {
      return $(this).css({
        display: 'none',
        opacity: 1
      });
    });
  };
  $.fn.gfxShake = function(options) {
    var distance, _ref, _ref2;
    if (options == null) {
      options = {};
    }
        if ((_ref = options.duration) != null) {
      _ref;
    } else {
      options.duration = 100;
    };
        if ((_ref2 = options.easing) != null) {
      _ref2;
    } else {
      options.easing = 'ease-out';
    };
    distance = options.distance || 20;
    $(this).gfx({
      translateX: "-" + distance + "px"
    }, options);
    $(this).gfx({
      translateX: "" + distance + "px"
    }, options);
    $(this).gfx({
      translateX: "-" + distance + "px"
    }, options);
    $(this).gfx({
      translateX: "" + distance + "px"
    }, options);
    return $(this).queueNext(function() {
      return $(this).transform({
        translateX: 0
      });
    });
  };
  $.fn.gfxBlip = function(options) {
    if (options == null) {
      options = {};
    }
    options.scale || (options.scale = '1.15');
    $(this).gfx({
      scale: options.scale
    }, options);
    return $(this).gfx({
      scale: '1'
    }, options);
  };
  $.fn.gfxExplodeIn = function(options) {
    if (options == null) {
      options = {};
    }
    options.scale || (options.scale = '3');
    $(this).queueNext(function() {
      return $(this).transform({
        scale: options.scale,
        opacity: '0',
        display: 'block'
      });
    });
    return $(this).gfx({
      scale: '1',
      opacity: '1'
    }, options);
  };
  $.fn.gfxExplodeOut = function(options) {
    if (options == null) {
      options = {};
    }
    options.scale || (options.scale = '3');
    $(this).queueNext(function() {
      return $(this).transform({
        scale: '1',
        opacity: '1'
      });
    });
    $(this).gfx({
      scale: options.scale,
      opacity: '0'
    }, options);
    if (options.reset !== false) {
      $(this).queueNext(function() {
        return $(this).transform({
          scale: '1',
          opacity: '1',
          display: 'none'
        });
      });
    }
    return this;
  };
  $.fn.gfxFlipIn = function(options) {
    if (options == null) {
      options = {};
    }
    $(this).queueNext(function() {
      return $(this).transform({
        rotateY: '180deg',
        scale: '.8',
        display: 'block'
      });
    });
    return $(this).gfx({
      rotateY: 0,
      scale: 1
    }, options);
  };
  $.fn.gfxFlipOut = function(options) {
    if (options == null) {
      options = {};
    }
    $(this).queueNext(function() {
      return $(this).transform({
        rotateY: 0,
        scale: 1
      });
    });
    $(this).gfx({
      rotateY: '-180deg',
      scale: '.8'
    }, options);
    if (options.reset !== false) {
      $(this).queueNext(function() {
        return $(this).transform({
          scale: 1,
          rotateY: 0,
          display: 'none'
        });
      });
    }
    return this;
  };
  $.fn.gfxRotateOut = function(options) {
    if (options == null) {
      options = {};
    }
    $(this).queueNext(function() {
      return $(this).transform({
        rotateY: 0
      }).fix();
    });
    $(this).gfx({
      rotateY: '-180deg'
    }, options);
    if (options.reset !== false) {
      $(this).queueNext(function() {
        return $(this).transform({
          rotateY: 0,
          display: 'none'
        }).unfix();
      });
    }
    return this;
  };
  $.fn.gfxRotateIn = function(options) {
    if (options == null) {
      options = {};
    }
    $(this).queueNext(function() {
      return $(this).transform({
        rotateY: '180deg',
        display: 'block'
      }).fix();
    });
    $(this).gfx({
      rotateY: 0
    }, options);
    $(this).queueNext(function() {
      return $(this).unfix();
    });
    return $ = jQuery;
  };
  $.fn.gfxSlideOut = function(options) {
    var distance, opacity;
    if (options == null) {
      options = {};
    }
    options.direction || (options.direction = 'right');
    distance = options.distance || 100;
    if (options.direction === 'left') {
      distance *= -1;
    }
    distance += "%";
    opacity = options.fade ? 0 : 1;
    $(this).gfx({
      translateX: distance,
      opacity: opacity
    }, options);
    return $(this).queueNext(function() {
      return $(this).transform({
        translateX: 0,
        opacity: 1,
        display: 'none'
      });
    });
  };
  $.fn.gfxSlideIn = function(options) {
    var distance, opacity;
    if (options == null) {
      options = {};
    }
    options.direction || (options.direction = 'right');
    distance = options.distance || 100;
    if (options.direction === 'left') {
      distance *= -1;
    }
    distance += "%";
    opacity = options.fade ? 0 : 1;
    $(this).queueNext(function() {
      return $(this).transform({
        translateX: distance,
        opacity: opacity,
        display: 'block'
      });
    });
    return $(this).gfx({
      translateX: 0,
      opacity: 1
    }, options);
  };
  $.fn.fix = function() {
    return $(this).each(function() {
      var element, parentOffset, styles;
      element = $(this);
      styles = element.offset();
      parentOffset = element.parent().offset();
      styles.left -= parentOffset.left;
      styles.top -= parentOffset.top;
      styles.position = 'absolute';
      return element.css(styles);
    });
  };
  $.fn.unfix = function() {
    return $(this).each(function() {
      var element;
      element = $(this);
      return element.css({
        position: '',
        top: '',
        left: ''
      });
    });
  };
  $ = jQuery;
  sides = {
    front: {
      rotateY: '0deg',
      rotateX: '0deg'
    },
    back: {
      rotateX: '-180deg',
      rotateX: '0deg'
    },
    right: {
      rotateY: '-90deg',
      rotateX: '0deg'
    },
    left: {
      rotateY: '90deg',
      rotateX: '0deg'
    },
    top: {
      rotateY: '0deg',
      rotateX: '-90deg'
    },
    bottom: {
      rotateY: '0deg',
      rotateX: '90deg'
    }
  };
  defaults = {
    width: 300,
    height: 300
  };
  $.fn.gfxCube = function(options) {
    var back, bottom, element, front, left, opts, right, tZ, top, wrapper;
    opts = $.extend({}, defaults, options);
    element = $(this);
    tZ = opts.translateZ || opts.width / 2;
    if (typeof tZ === 'number') {
      tZ += 'px';
    }
    element.transform({
      position: 'relative',
      width: opts.width,
      height: opts.height,
      '-webkit-perspective': '3000',
      '-moz-perspective': '3000',
      '-webkit-perspective-origin': '50% 50%',
      '-moz-perspective-origin': '50% 50%'
    });
    wrapper = $('<div />');
    wrapper.addClass('gfxCubeWrapper');
    wrapper.transform({
      position: 'absolute',
      width: '100%',
      height: '100%',
      left: 0,
      top: 0,
      overflow: 'visible',
      rotateY: '0deg',
      rotateX: '0deg',
      translateZ: "-" + tZ,
      '-webkit-transform-style': 'preserve-3d',
      '-moz-transform-style': 'preserve-3d',
      '-webkit-transform-origin': '50% 50%',
      '-moz-transform-origin': '50% 50%'
    });
    element.children().wrapAll(wrapper).css({
      display: 'block',
      position: 'absolute',
      width: '100%',
      height: '100%',
      left: 0,
      top: 0,
      overflow: 'hidden'
    });
    front = element.find('.front');
    back = element.find('.back');
    right = element.find('.right');
    left = element.find('.left');
    top = element.find('.top');
    bottom = element.find('.bottom');
    front.transform({
      rotateY: '0deg',
      translateZ: tZ
    });
    back.transform({
      rotateY: '180deg',
      translateZ: tZ
    });
    right.transform({
      rotateY: '90deg',
      translateZ: tZ
    });
    left.transform({
      rotateY: '-90deg',
      translateZ: tZ
    });
    top.transform({
      rotateX: '90deg',
      translateZ: tZ
    });
    bottom.transform({
      rotateX: '-90deg',
      translateZ: tZ
    });
    return $(this).bind('cube', function(e, type) {
      wrapper = element.find('.gfxCubeWrapper');
      return wrapper.gfx($.extend({}, {
        translateZ: "-" + tZ
      }, sides[type]));
    });
  };
  chromeRegex = /(Chrome)[\/]([\w.]+)/;
  chromeMatch = chromeRegex.exec(navigator.userAgent) || [];
  chrome11 = chromeRegex[1] && chromeRegex[2].test(/^12\./);
  if (!$.browser.webkit || chrome11) {
    $.fn.gfxCube = function(options) {
      var element, opts, wrapper;
      opts = $.extend({}, defaults, options);
      element = $(this);
      element.css({
        position: 'relative',
        width: opts.width,
        height: opts.height
      });
      wrapper = $('<div />');
      wrapper.addClass('gfxCubeWrapper');
      wrapper.transform({
        position: 'absolute',
        width: '100%',
        height: '100%',
        left: 0,
        top: 0,
        overflow: 'visible'
      });
      element.children().wrapAll(wrapper).css({
        display: 'block',
        position: 'absolute',
        width: '100%',
        height: '100%',
        left: 0,
        top: 0,
        overflow: 'hidden'
      });
      wrapper = element.find('.gfxCubeWrapper');
      wrapper.children('*:not(.front)').hide();
      return element.bind('cube', function(e, type) {
        wrapper.children().hide();
        return wrapper.children("." + type).show();
      });
    };
  }
  $ = jQuery;
  defaults = {
    width: 120,
    height: 120
  };
  $.fn.gfxFlip = function(options) {
    var back, front, opts;
    if (options == null) {
      options = {};
    }
    opts = $.extend({}, defaults, options);
    front = $(this).find('.front');
    back = $(this).find('.back');
    $(this).css({
      'position': 'relative',
      '-webkit-perspective': '600',
      '-moz-perspective': '600',
      '-webkit-transform-style': 'preserve-3d',
      '-moz-transform-style': 'preserve-3d',
      '-webkit-transform-origin': '50% 50%',
      '-moz-transform-origin': '50% 50%',
      'width': opts.width,
      'height': opts.height
    });
    front.add(back).css({
      position: 'absolute',
      width: '100%',
      height: '100%',
      display: 'block',
      '-webkit-backface-visibility': 'hidden',
      '-moz-backface-visibility': 'hidden'
    });
    back.transform({
      rotateY: '-180deg'
    });
    return $(this).bind('flip', function() {
      var flipped;
      $(this).toggleClass('flipped');
      flipped = $(this).hasClass('flipped');
      front.gfx({
        'rotateY': flipped ? '180deg' : '0deg'
      });
      return back.gfx({
        'rotateY': flipped ? '0deg' : '-180deg'
      });
    });
  };
  $ = jQuery;
  isOpen = function() {
    return !!$('#gfxOverlay').length;
  };
  close = function() {
    var overlay;
    overlay = $('#gfxOverlay');
    overlay.find('#gfxOverlayPanel').gfx({
      scale: '1.1',
      opacity: 0
    });
    overlay.gfx({
      background: 'rgba(0,0,0,0)'
    });
    return overlay.queueNext(function() {
      return overlay.remove();
    });
  };
  panelCSS = {
    opacity: 0,
    scale: 0.5,
    width: 500,
    height: 400
  };
  overlayStyles = {
    position: 'fixed',
    zIndex: 99,
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    background: 'rgba(0,0,0,0)'
  };
  $.gfxOverlay = function(element, options) {
    var overlay, panel, _base, _base2;
    if (options == null) {
      options = {};
    }
    if (isOpen()) {
      close();
    }
    element = $(element);
    if (element[0].tagName === 'SCRIPT') {
      element = element.html();
    } else {
      element = element.clone();
    }
    options.css || (options.css = {});
    (_base = options.css).width || (_base.width = options.width);
    (_base2 = options.css).height || (_base2.height = options.height);
    overlay = $('<div />').attr({
      'id': 'gfxOverlay'
    });
    overlay.css(overlayStyles);
    overlay.click(close);
    overlay.delegate('.close', 'click', close);
    overlay.bind('close', close);
    panel = $('<div />').attr({
      'id': 'gfxOverlayPanel'
    });
    panel.transform($.extend({}, panelCSS, options.css));
    panel.append(element);
    overlay.append(panel);
    $('body').append(overlay);
    overlay.delay().gfx({
      background: 'rgba(0,0,0,0.5)'
    }, {
      duration: options.duration
    });
    return panel.delay().gfx({
      scale: 1,
      opacity: 1
    });
  };
}).call(this);
