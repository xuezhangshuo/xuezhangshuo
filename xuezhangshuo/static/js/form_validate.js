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
