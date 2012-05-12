
$ ->

    $win = $(window)
    $nav = $('.subnav')
    navTop = $('.subnav').length and $('.subnav').offset().top - 40
    isFixed = false

    processScroll = ->
        scrollTop = $win.scrollTop()

        if scrollTop >= navTop and not isFixed
            isFixed = true
            $nav.addClass('subnav-fixed')

        else if scrollTop <= navTop and isFixed
            isFixed = false
            $nav.removeClass('subnav-fixed')


    processScroll()

    $win.on('scroll', processScroll)
