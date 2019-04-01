function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            //去除空白符
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // 这些HTTP方法不要求CSRF包含
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$('.btn1').click(function () {
    if ($('#contact_phone').val() == '') {
        $('.err3').html('手机号为空')
    } else {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken)
                }
            }
        });
        $.ajax({
            url: "http://127.0.0.1:8000/pylxh/note/",
            type: 'post',
            data: {
                'phone': $('#contact_phone').val(),
            },
            success: function (data) {
                alert(data.error3);
            }
        });
    }
});

$('.btn2').click(function () {
    console.log($('#contact_phone1').val());
    if ($('#contact_phone1').val() == '') {
        $('.err3').html('手机号为空')
    } else {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken)
                }
            }
        });

        $.ajax({
            url: "http://127.0.0.1:8000/pylxh/note/",
            type: 'post',
            data: {
                'phone': $('#contact_phone1').val(),
            },
            success: function (data) {
                alert(data.error3);
            }
        });
    }
});