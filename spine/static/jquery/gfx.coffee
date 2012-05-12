$ = @jQuery

throw 'jQuery required' unless $

defaults =
  duration: 400
  queue: true
  easing: ''

vendor = if $.browser.mozilla then 'moz'
vendor or= 'webkit'
prefix = "-#{vendor}-"

vendorNames = n =
  transition: "#{prefix}transition"
  transform: "#{prefix}transform"
  transitionEnd: "#{vendor}TransitionEnd"

transformTypes = [
  'scale', 'scaleX', 'scaleY', 'scale3d',
  'rotate', 'rotateX', 'rotateY', 'rotateZ', 'rotate3d',
  'translate', 'translateX', 'translateY', 'translateZ', 'translate3d',
  'skew', 'skewX', 'skewY',
  'matrix', 'matrix3d', 'perspective'
]

# Internal helper functions

$.fn.queueNext = (callback, type) ->
    type or= "fx";

    @queue ->
      callback.apply(this, arguments)
      setTimeout =>
        jQuery.dequeue(this, type)

$.fn.emulateTransitionEnd = (duration) ->
  called = false
  $(@).one(n.transitionEnd, -> called = true)
  callback = => $(@).trigger(n.transitionEnd) unless called
  setTimeout(callback, duration)

# Helper function for easily adding transforms

$.fn.transform = (properties) ->
  transforms = []

  for key, value of properties when key in transformTypes
    transforms.push("#{key}(#{value})")
    delete properties[key]

  if transforms.length
    properties[n.transform] = transforms.join(' ')

  $(@).css(properties)

$.fn.gfx = (properties, options) ->
  opts = $.extend({}, defaults, options)

  properties[n.transition] = "all #{opts.duration}ms #{opts.easing}"

  callback = ->
    $(@).css(n.transition, '')
    opts.complete?.apply(this, arguments)
    $(@).dequeue()

  @[ if opts.queue is false then 'each' else 'queue' ] ->
    $(@).one(n.transitionEnd, callback)
    $(@).transform(properties)

    # Sometimes the event doesn't fire, so we have to fire it manually
    $(@).emulateTransitionEnd(opts.duration + 50)

# Additional Effects

$.fn.gfxPopIn = (options = {}) ->
  options.scale ?= '.2'

  $(@).queueNext ->
    $(@).transform
      '-webkit-transform-origin': '50% 50%'
      '-moz-transform-origin': '50% 50%'
      scale:   options.scale
      opacity: '0'
      display: 'block'

  $(@).gfx({
    scale:   '1'
    opacity: '1'
  }, options)

$.fn.gfxPopOut = (options) ->
  $(@).queueNext ->
    $(@).transform
      '-webkit-transform-origin': '50% 50%'
      '-moz-transform-origin': '50% 50%'
      scale:   '1'
      opacity: '1'
  $(@).gfx({
    scale:   '.2'
    opacity: '0'
  }, options)

  $(@).queueNext ->
    $(@).transform
      display: 'none'
      opacity: '1'
      scale:   '1'

$.fn.gfxFadeIn = (options = {}) ->
  options.duration ?= 1000
  $(@).queueNext ->
    $(@).css
      display: 'block'
      opacity: '0'
  $(@).gfx({opacity: 1}, options);

$.fn.gfxFadeOut = (options = {}) ->
  $(@).queueNext ->
    $(@).css
      opacity: 1
  $(@).gfx({opacity: 0}, options)
  $(@).queueNext ->
    $(@).css
      display: 'none'
      opacity: 1

$.fn.gfxShake = (options = {}) ->
  options.duration ?= 100
  options.easing   ?= 'ease-out'
  distance = options.distance or 20
  $(@).gfx({translateX: "-#{distance}px"}, options)
  $(@).gfx({translateX: "#{distance}px"}, options)
  $(@).gfx({translateX: "-#{distance}px"}, options)
  $(@).gfx({translateX: "#{distance}px"}, options)
  $(@).queueNext ->
    $(@).transform(translateX: 0)

$.fn.gfxBlip = (options = {}) ->
  options.scale or= '1.15'
  $(@).gfx({scale: options.scale}, options)
  $(@).gfx({scale: '1'}, options)

$.fn.gfxExplodeIn = (options = {}) ->
  options.scale or= '3'
  $(@).queueNext ->
    $(@).transform(scale: options.scale, opacity: '0', display: 'block')
  $(@).gfx({scale: '1', opacity: '1'}, options)

$.fn.gfxExplodeOut = (options = {}) ->
  options.scale or= '3'
  $(@).queueNext ->
    $(@).transform(scale: '1', opacity: '1')
  $(@).gfx({scale: options.scale, opacity: '0'}, options)

  unless options.reset is false
    $(@).queueNext ->
      $(@).transform(scale: '1', opacity: '1', display: 'none')
  this

$.fn.gfxFlipIn = (options = {}) ->
  $(@).queueNext ->
    $(@).transform(rotateY: '180deg', scale: '.8', display: 'block')
  $(@).gfx({rotateY: 0, scale: 1}, options)

$.fn.gfxFlipOut = (options = {}) ->
  $(@).queueNext ->
    $(@).transform(rotateY: 0, scale: 1)
  $(@).gfx({rotateY: '-180deg', scale: '.8'}, options)

  unless options.reset is false
    $(@).queueNext ->
      $(@).transform(scale: 1, rotateY: 0, display: 'none')
  this

$.fn.gfxRotateOut = (options = {}) ->
  $(@).queueNext ->
    $(@).transform(rotateY: 0).fix()
  $(@).gfx({rotateY: '-180deg'}, options)

  unless options.reset is false
    $(@).queueNext ->
      $(@).transform(rotateY: 0, display: 'none').unfix()
  @

$.fn.gfxRotateIn = (options = {}) ->
  $(@).queueNext ->
    $(@).transform(rotateY: '180deg', display: 'block').fix()
  $(@).gfx({rotateY: 0}, options)
  $(@).queueNext -> $(@).unfix()

  $ = jQuery

$.fn.gfxSlideOut = (options = {}) ->
  options.direction or= 'right'

  distance = options.distance or 100
  distance *= -1 if options.direction is 'left'
  distance += "%"

  opacity = if options.fade then 0 else 1

  $(@).gfx({translateX: distance, opacity: opacity}, options)
  $(@).queueNext ->
    $(@).transform(translateX: 0, opacity: 1, display: 'none')

$.fn.gfxSlideIn = (options = {}) ->
  options.direction or= 'right'

  distance = options.distance or 100
  distance *= -1 if options.direction is 'left'
  distance += "%"

  opacity = if options.fade then 0 else 1

  $(@).queueNext ->
    $(@).transform(translateX: distance, opacity: opacity, display: 'block')
  $(@).gfx({translateX: 0, opacity: 1}, options)

$.fn.fix = ->
  $(@).each ->
    element = $(@)
    styles  = element.offset()
    parentOffset = element.parent().offset()
    styles.left -= parentOffset.left
    styles.top  -= parentOffset.top
    styles.position = 'absolute'
    element.css(styles)

$.fn.unfix = ->
  $(@).each ->
    element = $(@)
    element.css(position: '', top:'', left: '')

$ = jQuery

sides =
  front:  {rotateY: '0deg',    rotateX: '0deg'}
  back:   {rotateX: '-180deg', rotateX: '0deg'}
  right:  {rotateY: '-90deg',  rotateX: '0deg'}
  left:   {rotateY: '90deg',   rotateX: '0deg'}
  top:    {rotateY: '0deg',    rotateX: '-90deg'}
  bottom: {rotateY: '0deg',    rotateX: '90deg'}

defaults =
  width: 300
  height: 300

$.fn.gfxCube = (options) ->
  opts = $.extend({}, defaults, options)

  element = $(@)

  tZ = opts.translateZ or opts.width / 2
  tZ += 'px' if typeof tZ is 'number'

  element.transform
    position: 'relative'
    width:  opts.width
    height: opts.height
    '-webkit-perspective': '3000'
    '-moz-perspective': '3000'
    '-webkit-perspective-origin': '50% 50%'
    '-moz-perspective-origin': '50% 50%'

  wrapper = $('<div />')
  wrapper.addClass('gfxCubeWrapper')
  wrapper.transform
    position: 'absolute'
    width: '100%'
    height: '100%'
    left: 0
    top: 0
    overflow: 'visible'
    rotateY: '0deg'
    rotateX: '0deg'
    translateZ: "-#{tZ}"
    '-webkit-transform-style': 'preserve-3d'
    '-moz-transform-style': 'preserve-3d'
    '-webkit-transform-origin': '50% 50%'
    '-moz-transform-origin': '50% 50%'

  element.children().wrapAll(wrapper).css
    display: 'block'
    position: 'absolute'
    width: '100%'
    height: '100%'
    left: 0
    top: 0
    overflow: 'hidden'

  front   = element.find('.front')
  back    = element.find('.back')
  right   = element.find('.right')
  left    = element.find('.left')
  top     = element.find('.top')
  bottom  = element.find('.bottom')

  front.transform   rotateY: '0deg',   translateZ: tZ
  back.transform    rotateY: '180deg', translateZ: tZ
  right.transform   rotateY: '90deg',  translateZ: tZ
  left.transform    rotateY: '-90deg', translateZ: tZ
  top.transform     rotateX: '90deg',  translateZ: tZ
  bottom.transform  rotateX: '-90deg', translateZ: tZ

  $(@).bind 'cube', (e, type) ->
    wrapper = element.find('.gfxCubeWrapper')
    wrapper.gfx($.extend({}, {translateZ: "-#{tZ}"}, sides[type]))

# Disable cubes in Firefox / Chrome < 12
chromeRegex = /(Chrome)[\/]([\w.]+)/
chromeMatch = chromeRegex.exec( navigator.userAgent ) or []
chrome11    = chromeRegex[1] and chromeRegex[2].test(/^12\./)

if not $.browser.webkit or chrome11
  $.fn.gfxCube = (options) ->
    opts = $.extend({}, defaults, options)

    element = $(@)

    element.css
      position: 'relative'
      width:  opts.width
      height: opts.height

    wrapper = $('<div />')
    wrapper.addClass('gfxCubeWrapper')
    wrapper.transform
      position: 'absolute'
      width: '100%'
      height: '100%'
      left: 0
      top: 0
      overflow: 'visible'

    element.children().wrapAll(wrapper).css
      display: 'block'
      position: 'absolute'
      width: '100%'
      height: '100%'
      left: 0
      top: 0
      overflow: 'hidden'

    wrapper = element.find('.gfxCubeWrapper')

    wrapper.children('*:not(.front)').hide()
    element.bind 'cube', (e, type) ->
      wrapper.children().hide()
      wrapper.children(".#{type}").show()


$ = jQuery

defaults =
  width: 120
  height: 120

$.fn.gfxFlip = (options = {}) ->
  opts = $.extend({}, defaults, options)

  front = $(@).find('.front')
  back  = $(@).find('.back')

  $(@).css(
    'position': 'relative'
    '-webkit-perspective': '600'
    '-moz-perspective': '600'
    '-webkit-transform-style': 'preserve-3d'
    '-moz-transform-style': 'preserve-3d'
    '-webkit-transform-origin': '50% 50%'
    '-moz-transform-origin': '50% 50%'
    'width': opts.width;
    'height': opts.height;
  )

  front.add(back).css
    position: 'absolute'
    width:    '100%'
    height:   '100%'
    display:  'block'
    '-webkit-backface-visibility': 'hidden'
    '-moz-backface-visibility': 'hidden'

  back.transform
    rotateY: '-180deg'

  $(@).bind 'flip', ->
    $(@).toggleClass('flipped')
    flipped = $(@).hasClass('flipped')

    front.gfx('rotateY': if flipped then '180deg' else '0deg')
    back.gfx('rotateY': if flipped then '0deg' else '-180deg')

$ = jQuery

isOpen = ->
  !!$('#gfxOverlay').length

close = ->
  overlay = $('#gfxOverlay')
  overlay.find('#gfxOverlayPanel').gfx(scale: '1.1', opacity: 0)
  overlay.gfx(background: 'rgba(0,0,0,0)')
  overlay.queueNext -> overlay.remove()

panelCSS =
  opacity:    0
  scale:      0.5
  width:      500
  height:     400

overlayStyles =
  position:   'fixed'
  zIndex:     99
  top:        0
  left:       0
  width:      '100%'
  height:     '100%'
  background: 'rgba(0,0,0,0)'

$.gfxOverlay = (element, options = {}) ->
  close() if isOpen()

  element = $(element)
  if element[0].tagName is 'SCRIPT'
    element = element.html()
  else
    element = element.clone()

  options.css or= {}
  options.css.width  or= options.width
  options.css.height or= options.height

  overlay = $('<div />').attr('id': 'gfxOverlay')
  overlay.css(overlayStyles)
  overlay.click(close)
  overlay.delegate('.close', 'click', close)
  overlay.bind('close', close)

  panel = $('<div />').attr('id': 'gfxOverlayPanel')
  panel.transform($.extend({}, panelCSS, options.css))

  panel.append(element)
  overlay.append(panel)
  $('body').append(overlay)

  overlay.delay().gfx({background: 'rgba(0,0,0,0.5)'}, {duration: options.duration})
  panel.delay().gfx({scale: 1, opacity: 1})

