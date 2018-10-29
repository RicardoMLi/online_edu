//修改个人中心邮箱验证码
function sendCodeChangeEmail($btn){
    var verify = verifyDialogSubmit(
        [
          {id: '#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true}
        ]
    );
    if(!verify){
       return;
    }
    $.ajax({
        cache: false,
        type: "get",
        dataType:'json',
        url:"/user/send_verifycode/",
        data:$('#jsChangeEmailForm').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $btn.val("发送中...");
            $btn.attr('disabled',true);
        },
        success: function(data){
            if(data.status == 'success'){
                Dml.fun.showErrorTips($('#jsChangeEmailTips'), "邮箱验证码已发送");
            }else if(data.status == 'fail'){
                 Dml.fun.showValidateError($('#jsChangeEmail'), data.msg);
            }
        },
        complete: function(XMLHttpRequest){
            $btn.val("获取验证码");
            $btn.removeAttr("disabled");
        }
    });

}


//第三方登录用户修改邮箱
// function changeEmailSubmit2($btn){
//     var email = $("#jsChangeEmail").val();
//     var csrftoken = getCookie('csrftoken');
//     $.ajax({
//         cache: false,
//         type: 'POST',
//         url:"/user/modify_email_third/",
//         data:{"email":email},
//         async: true,
//         beforeSend:function(xhr,settings){
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//             $btn.val("激活码发送中...");
//             $btn.attr('disabled',true);
//         },
//         success: function(data) {
//             if(data.status == "success"){
//                 $("#jsChangeEmailDialog").hide();
//                 alert("激活码已发送至您的邮箱,请注意查收");
//                 window.location.href = '/user/login/';
//             }else if(data.status == "fail"){
//                  Dml.fun.showValidateError($('#jsChangeEmail'), data.msg);
//             }
//         },
//     });
// }

//个人资料邮箱修改
function changeEmailSubmit($btn){
var verify = verifyDialogSubmit(
        [
          {id: '#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true},
        ]
    );
    if(!verify){
       return;
    }
    $.ajax({
        cache: false,
        type: 'post',
        dataType:'json',
        url:"/user/modify_email/",
        data:$('#jsChangeEmailForm').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $btn.val("发送中...");
            $btn.attr('disabled',true);
            $("#jsChangeEmailTips").html("验证中...").show(500);
        },
        success: function(data) {
            if(data.status == "success"){
                Dml.fun.showErrorTips($('#jsChangePhoneTips'), "邮箱信息更新成功");
                setTimeout(function(){location.reload();},1000);
            }else if(data.status == "fail"){
                 Dml.fun.showValidateError($('#jsChangeEmail'), data.msg);
            }
        },
        complete: function(XMLHttpRequest){
            $btn.val("完成");
            $btn.removeAttr("disabled");
        }
    });
}

function check_mobile(mobile){
    var myreg=/^[1][3,4,5,7,8][0-9]{9}$/;

    if(mobile == ""){
        Dml.fun.showValidateError($('#jsChangeMobile'), '手机号码不能为空');
        return false;
    }

    if(!myreg.test(mobile)){
        Dml.fun.showValidateError($('#jsChangeMobile'), '手机号码非法');
        return false;
    }

    return true;
}

function sendCodeChangePhone($btn){
    var mobile = $("#jsChangeMobile").val();

    if(!check_mobile(mobile))
        return;

    $.ajax({
        cache: false,
        type: "post",
        dataType:'json',
        url:"/user/send_mobilecode/",
        data:$('#jsChangePhoneForm').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $btn.attr('disabled',true);
        },
        success:function(data){
            if(data.status == 'success'){
                var duration = 120;
                var timeObj = setInterval(function (){
                    duration = duration - 1;
                    $("#jsChangePhoneCodeBtn").val(duration+"秒后获取验证码");
                    //禁用点击事件
                    $("#jsChangePhoneCodeBtn").attr('disabled',true);
                    if (1 == duration) {
                        clearInterval(timeObj);
                        //解除禁用点击事件
                        $("#jsChangePhoneCodeBtn").attr('disabled',false);
                        $("#jsChangePhoneCodeBtn").val("获取验证码")
                    }
                }, 1000, 120);
            }else if(data.status == 'fail'){
                 Dml.fun.showValidateError($('#jsChangeMobile'), data.msg);
            }               
        },
        complete: function(XMLHttpRequest){
            $btn.val("获取验证码");
            $btn.removeAttr("disabled");
        }
    })
}

function check_code(code){
    var myreg = /^[0-9]{4}$/;

    if(code == ""){
        Dml.fun.showValidateError($('#jsChangeMobile'), '验证码不能为空');
        return false;
    }

    if(!myreg.test(code)){
        Dml.fun.showValidateError($('#jsChangePhoneCode'), '验证码格式错误');
        return false;
    }

    return true;

}

//个人资料手机号码修改
function changePhoneSubmit($btn){
    var mobile = $("#jsChangeMobile").val();
    var code = $("#jsChangePhoneCode").val();

    if(!check_mobile(mobile)){
        return;
    }

    if(!check_code(code)){
        return;
    }


    $.ajax({
        cache: false,
        type: 'post',
        dataType:'json',
        url:"/user/modify_mobile/",
        data:$('#jsChangePhoneForm').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $btn.attr('disabled',true);
        },
        success: function(data) {
            if(data.status == "success"){
                Dml.fun.showErrorTips($('#jsChangePhoneTips'), "手机号码绑定成功");
                $btn.attr('disabled',false);
                setTimeout(function(){location.reload();},1000);
            }else if(data.status == "fail"){
                if(data.msg == '手机号码不能为空' || data.msg == '手机号码非法')
                    Dml.fun.showValidateError($('#jsChangePhone'), data.msg);
                else
                    Dml.fun.showValidateError($('#jsChangePhoneCode'), data.msg);
            }
        },
        complete: function(XMLHttpRequest){
            $btn.val("完成");
            $btn.removeAttr("disabled");
        }
    });
}

$(function(){
    //个人资料修改密码
    $('#jsUserResetPwd').on('click', function(){
        Dml.fun.showDialog('#jsResetDialog', '#jsResetPwdTips');
    });

    $('#jsResetPwdBtn').click(function(){
        $.ajax({
            cache: false,
            type: "POST",
            dataType:'json',
            url:"/user/update_password/",
            data:$('#jsResetPwdForm').serialize(),
            async: true,
            success: function(data) {
                if(data.password1){
                    Dml.fun.showValidateError($("#pwd"), data.password1);
                }else if(data.password2){
                    Dml.fun.showValidateError($("#repwd"), data.password2);
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title:'提交成功',
                        h2:'修改密码成功，请重新登录!',
                    });
                    Dml.fun.winReload();
                }else if(data.msg){
                    Dml.fun.showValidateError($("#pwd"), data.msg);
                    Dml.fun.showValidateError($("#repwd"), data.msg);
                }
            }
        });
    });

    //个人资料头像
    $('.js-img-up').uploadPreview({ Img: ".js-img-show", Width: 94, Height: 94 ,Callback:function(){
        $('#jsAvatarForm').submit();
    }});

    $('#jsChangeEmailButton').click(function(){
        Dml.fun.showDialog('#jsChangeEmailDialog', '#jsChangePhoneTips' ,'jsChangeEmailTips');    
    });
    $('.changephone_btn').click(function(){
        Dml.fun.showDialog('#jsChangePhoneDialog','#jsChangePhoneTips')
    });
    $('#jsChangeEmailCodeBtn').on('click', function(){
        sendCodeChangeEmail($(this));
    });
    $('#jsChangeEmailBtn').on('click', function(){
        changeEmailSubmit($(this));    
    });
    $('#jsChangePhoneCodeBtn').on('click', function(){
        sendCodeChangePhone($(this));
    });   
    $('#jsChangePhoneBtn').on('click', function(){
        changePhoneSubmit($(this));
    });

    //input获得焦点样式
    $('.perinform input[type=text]').focus(function(){
        $(this).parent('li').addClass('focus');
    });
    $('.perinform input[type=text]').blur(function(){
        $(this).parent('li').removeClass('focus');
    });

    laydate({
        elem: '#birth_day',
        format: 'YYYY-MM-DD',
        max: laydate.now()
    });

    verify(
        [
            {id: '#nick_name', tips: Dml.Msg.epNickName, require: true}
        ]
    );
    //保存个人资料
    $('#jsEditUserBtn').on('click', function(){
        var _self = $(this),
            $jsEditUserForm = $('#jsEditUserForm')
            verify = verifySubmit(
            [
                {id: '#nick_name', tips: Dml.Msg.epNickName, require: true}
            ]
        );
        if(!verify){
           return;
        }
        $.ajax({
            cache: false,
            type: 'post',
            dataType:'json',
            url:"/user/user_info/",
            data:$jsEditUserForm.serialize(),
            async: true,
            beforeSend:function(XMLHttpRequest){
                _self.val("保存中...");
                _self.attr('disabled',true);
            },
            success: function(data) {
                if(data.nickname){
                    _showValidateError($('#nick_name'), data.nickname);
                }else if(data.birday){
                   _showValidateError($('#birth_day'), data.birthday);
                }else if(data.address){
                   _showValidateError($('#address'), data.address);
                }else if(data.status == "fail"){
                     Dml.fun.showTipsDialog({
                        title: '保存失败',
                        h2: data.msg
                    });
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title: '保存成功',
                        h2: '个人信息修改成功！'
                    });
                    setTimeout(function(){window.location.href = window.location.href;},1500);
                }
            },
            complete: function(XMLHttpRequest){
                _self.val("保存");
                _self.removeAttr("disabled");
            }
        });
    });

});