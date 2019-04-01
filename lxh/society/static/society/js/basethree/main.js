$('.point-categ').click(function () {
    $('.title1_left_point').removeClass('one-point');
    $(this).children('.title1_left_point').addClass('one-point');
    $('.point-categ').removeClass('black');
    $(this).addClass('black');
    turnpage($(this).attr('href'));
});

$('.flash-img').click(function () {
	$('.flash-txt').not($(this).parent().parent().children('.flash-txt')).hide();
    $(this).parent().parent().children('.flash-txt').toggle();
    $('.ablack').not($(this).parent().children().children('.ablack')).removeClass('skyblue');
    $(this).parent().children().children('.ablack').toggleClass('skyblue');
    $('.flash-img').not($(this)).attr({'src': "/static/society/image/b_n.png"});
    if ($(this).attr('src') == "/static/society/image/b_n.png" ) {
        $(this).attr({'src': "/static/society/image/b_s.png"});
    } else {
        $(this).attr({'src': "/static/society/image/b_n.png"});
    }

});


function turnpage(url) {
	var url0 = document.URL;
	var num = url0.indexOf('?');
	var oldurl;
	if(num == -1) {
		oldurl = url0;
	} else {
		oldurl = url0.slice(0, num);
	}
	var newurl = oldurl + '?' + url;
	history.pushState(null, null, newurl);
	var ajaxurl = url ;

	$.ajax({
		type: "get",
		url: ajaxurl,
		success: function(html) {
			$('.ba_left_bot').html(html);
		}
	});
}






