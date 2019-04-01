$('.btn-cat').click(function () {
    $('span').filter('.iss-but').css({'color': '#333333', 'border-color': ' #E9E9E9'});
    $(this).parent().children().css({'color': '#1992EF', 'border-color': '#1992EF'});
});


$('.pay-input').click(function () {
    $('.level-bot-div>div').css({'border-color': ' #D9D9D9'});
   $(this).parent().children().filter('div').css({'border-color': '#1992EF'});
    var ht = $(this).parent().children().children().children('.f-sma').html();
    if (ht.indexOf('￥') == -1) {
        h = ht.split('积');
        $('.pay-money').html(h[0]);
    } else {
        $('.pay-money').html(ht);
    }

});


$('.pay-name').click(function () {
   $('.pay-img').css({'border-color': ' #D9D9D9'});
   $(this).parent().css({'border-color': '#1992EF'});
});

if ($('.alert-pay').html() == '余额不足') {
    alert($('.alert-pay').html());
    $('.alert-pay').html('')
}