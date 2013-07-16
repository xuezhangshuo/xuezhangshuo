function validateLoginForm()
{
    var loginForm = document.forms["loginForm"];
    var x = loginForm["username"].value;
    var atpos = x.indexOf("@");
    var dotpos = x.lastIndexOf(".");
    if (atpos<1 || dotpos<atpos+2 || dotpos+2>=x.length)
    {
        var errorPara = document.getElementById('error');
        if (!errorPara) {
            var notEmail = document.createElement("p");
            notEmail.id = "error";
            notEmail.innerHTML = "错误的账号类型";
            notEmail.style.color = "red";
            var parentDiv = loginForm.parentNode;
            parentDiv.insertBefore(notEmail, loginForm);
        }
        else errorPara.innerHTML = "错误的账号类型";
        return false;
    }
}

$(document).ready(function () {
    $('#reg').validate({ // initialize the plugin
        rules: {
            email: {
                required: true,
                email: true
            },
            name: {
                required: true,
                maxlength: 20
            },
            password: {
                required: true,
                minlength: 6,
                maxlength: 20
            },
            password_again: {
                equalTo: "#id_password"
            }
        },
        messages: {
            email: "请输入电子邮件",
            name: "请输入真实姓名",
            password: {
                required: "请输入密码",
                minlength: "密码长度为6~20位"
            },
            password_again: "两次密码输入不一致"
        },
        errorPlacement: function(error, element) {
            var ele_name = error.attr("for").substring(3);
            var err_element = document.getElementById("err_"+ele_name);
            if (err_element) {
                err_element.parentNode.removeChild(err_element);
            }
            error.css('color', 'red');
            error.appendTo( element.prev() );
        },
        errorElement: "span",
        submitHandler: function(form) {
            $(form).ajaxSubmit(saveOptions);
        }
      });
});