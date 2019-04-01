$('.role').click(function () {
    $('.role-sele').toggle();
    $('#login,#login-pri,.forget-pass>a,.check-pas').toggleClass('mohu');
});

$('.role-sele>div').click(function (event) {
    $('.role-sele').hide();
    $('.role-stu').html($(this).html());
    $('#login,#login-pri,.forget-pass>a,.check-pas').removeClass('mohu');
    $('#contact_role').val($(this).html());
    if ($('.role-stu').html() == '社团负责人') {
        $('.pri-check').show();
        $('.stu-check').hide();
    } else {
        $('.pri-check').hide();
        $('.stu-check').show();
    }

});


//用户名验证
function namefocu() {
    username = $('#contact_name').val();
    if (username.length > 20 || username.length < 4) {
        $('.err1').html('用户名范围4-20');
    }
}

function nameblus(){
    $('.err1').html('');
    username = $('#contact_name').val();
    if (username == '') {
        $('.err1').html("用户名不能为空");
        return false
    }
    if (username.length > 20 || username.length < 4) {
        $('.err1').html('用户名范围4-20');
        return false
    }
}


//密码验证
function passfocu() {
    username = $('#contact_pass').val();
    if (username.length > 32 || username.length < 6) {
        $('.err2').html('字母开头，范围6-20');
    }
}

function passblus() {
    $('.err2').html('');
    pass = $('#contact_pass').val();
    if (pass == '') {
        $('.err2').html("密码不能为空");
        return false
    }
    if (pass.length > 20 || pass.length < 6) {
        $('.err2').html('密码范围6-20');
        return false
    }
}

function pass2blus() {
    $('.err21').html('');
    pass = $('#contact_pass').val();
    if ($('#contact_pass_new').val() != pass) {
        $('.err21').html('两次密码不一致');
    }
}

//手机号验证
function phofocu() {
    username = $('#contact_phone').val();
    if (username.length != 11) {
        $('.err3').html('手机号11位');
    }
}

function phoblus() {
    $('.err3').html('');
    pass = $('#contact_phone').val();
    if (pass == '') {
        $('.err3').html("手机号不能为空");
        return false
    }
    if (pass.length != 11) {
        $('.err3').html('手机号11位');
        return false
    }
}


//pri
//用户名验证
function namefocu1() {
    username = $('#contact_name1').val();
    if (username.length > 20 || username.length < 4) {
        $('.err1').html('用户名范围4-20');
    }
}

function nameblus1(){
    $('.err1').html('');
    username = $('#contact_name1').val();
    if (username == '') {
        $('.err1').html("用户名不能为空");
        return false
    }
    if (username.length > 20 || username.length < 4) {
        $('.err1').html('用户名范围4-20');
        return false
    }
}


//密码验证
function passfocu1() {
    username = $('#contact_pass1').val();
    if (username.length > 32 || username.length < 6) {
        $('.err2').html('密码范围6-20');
    }
}

function passblus1() {
    $('.err2').html('');
    pass = $('#contact_pass1').val();
    if (pass == '') {
        $('.err2').html("密码不能为空");
        return false
    }
    if (pass.length > 20 || pass.length < 6) {
        $('.err2').html('密码范围6-20');
        return false
    }
}

function pass2blus1() {
    $('.err21').html('');
    pass = $('#contact_pass1').val();
    if ($('#contact_pass_new1').val() != pass) {
        $('.err21').html('两次密码不一致');
    }
}

//手机号验证
function phofocu1() {
    username = $('#contact_phone1').val();
    if (username.length != 11) {
        $('.err3').html('手机号11位');
    }
}

function phoblus1() {
    $('.err3').html('');
    pass = $('#contact_phone1').val();
    if (pass == '') {
        $('.err3').html("手机号不能为空");
        return false
    }
    if (pass.length != 11) {
        $('.err3').html('手机号11位');
        return false
    }
}

$(document).ready(function () {
    var t1 = window.setTimeout(refreshCount, 1000*60);
    function refreshCount() {
        $('.error').html('');
    }
    window.clearTimeout(t1);
});
