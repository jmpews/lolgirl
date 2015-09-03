$(document).ready(function () {
    $('.product').each(function (i, el) {
        $(el).find('.make3D').hover(function () {
            $(this).parent().css('z-index', '20');
            $(this).addClass('animate');
            $(this).find('div.carouselNext, div.carouselPrev').addClass('visible');
        }, function () {
            $(this).removeClass('animate');
            $(this).parent().css('z-index', '1');
            $(this).find('div.carouselNext, div.carouselPrev').removeClass('visible');
        });
        $(el).find('.view_gallery').click(function () {
            $(el).find('div.carouselNext, div.carouselPrev').removeClass('visible');
            $(el).find('.make3D').addClass('flip-10');
            setTimeout(function () {
                $(el).find('.make3D').removeClass('flip-10').addClass('flip90').find('div.shadow').show().fadeTo(80, 1, function () {
                    $(el).find('.product-front, .product-front div.shadow').hide();
                });
            }, 50);
            setTimeout(function () {
                $(el).find('.make3D').removeClass('flip90').addClass('flip190');
                $(el).find('.product-back').show().find('div.shadow').show().fadeTo(90, 0);
                setTimeout(function () {
                    $(el).find('.make3D').removeClass('flip190').addClass('flip180').find('div.shadow').hide();
                    setTimeout(function () {
                        $(el).find('.make3D').css('transition', '100ms ease-out');
                        $(el).find('.cx, .cy').addClass('s1');
                        setTimeout(function () {
                            $(el).find('.cx, .cy').addClass('s2');
                        }, 100);
                        setTimeout(function () {
                            $(el).find('.cx, .cy').addClass('s3');
                        }, 200);
                        $(el).find('div.carouselNext, div.carouselPrev').addClass('visible');
                    }, 100);
                }, 100);
            }, 150);
        });
        $(el).find('.flip-back').click(function () {
            $(el).find('.make3D').removeClass('flip180').addClass('flip190');
            setTimeout(function () {
                $(el).find('.make3D').removeClass('flip190').addClass('flip90');
                $(el).find('.product-back div.shadow').css('opacity', 0).fadeTo(100, 1, function () {
                    $(el).find('.product-back, .product-back div.shadow').hide();
                    $(el).find('.product-front, .product-front div.shadow').show();
                });
            }, 50);
            setTimeout(function () {
                $(el).find('.make3D').removeClass('flip90').addClass('flip-10');
                $(el).find('.product-front div.shadow').show().fadeTo(100, 0);
                setTimeout(function () {
                    $(el).find('.product-front div.shadow').hide();
                    $(el).find('.make3D').removeClass('flip-10').css('transition', '100ms ease-out');
                    $(el).find('.cx, .cy').removeClass('s1 s2 s3');
                }, 100);
            }, 150);
        });
        makeCarousel(el);
    });
    function makeCarousel(el) {
        var carousel = $(el).find('.carousel ul');
        var carouselSlideWidth = 265;
        var carouselWidth = 0;
        var isAnimating = false;
        var currSlide = 0;
        $(carousel).attr('rel', currSlide);
        $(carousel).find('li').each(function () {
            carouselWidth += carouselSlideWidth;
        });
        $(carousel).css('width', carouselWidth);
        $(el).find('div.carouselNext').on('click', function () {
            var currentLeft = Math.abs(parseInt($(carousel).css('left')));
            var newLeft = currentLeft + carouselSlideWidth;
            if (newLeft == carouselWidth || isAnimating === true) {
                return;
            }
            $(carousel).css({
                'left': '-' + newLeft + 'px',
                'transition': '300ms ease-out'
            });
            isAnimating = true;
            currSlide++;
            $(carousel).attr('rel', currSlide);
            setTimeout(function () {
                isAnimating = false;
            }, 300);
        });
        $(el).find('div.carouselPrev').on('click', function () {
            var currentLeft = Math.abs(parseInt($(carousel).css('left')));
            var newLeft = currentLeft - carouselSlideWidth;
            if (newLeft < 0 || isAnimating === true) {
                return;
            }
            $(carousel).css({
                'left': '-' + newLeft + 'px',
                'transition': '300ms ease-out'
            });
            isAnimating = true;
            currSlide--;
            $(carousel).attr('rel', currSlide);
            setTimeout(function () {
                isAnimating = false;
            }, 300);
        });
    }

});