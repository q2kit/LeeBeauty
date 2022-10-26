document.getElementById("btn-signin").addEventListener("click", function () {

    document.getElementById("errormsg").innerHTML = "";
    document.getElementById("successmsg").innerHTML = "";

    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    if (email == "") {
        document.getElementById("errormsg").innerHTML = "Email/SĐT không được để trống";
        document.getElementById("email").focus();
        return;
    }

    if (password == "") {
        document.getElementById("errormsg").innerHTML = "Mật khẩu không được để trống";
        document.getElementById("password").focus();
        return;
    }

    var fd = new FormData();
    fd.append("email", email);
    fd.append("password", password);
    fd.append("csrfmiddlewaretoken", document.getElementsByName("csrfmiddlewaretoken")[0].value);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/sign-in/", true);
    xhr.withCredentials = true;
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            var response = JSON.parse(xhr.responseText);
            if (response["success"] == true) {
                document.getElementById("successmsg").innerHTML = "Đăng nhập thành công";
                setTimeout(function () {
                    let url = new URL(window.location.href);
                    let next = url.searchParams.get("next") || "/";
                    window.location.href = next;
                }, 3000);
            } else {
                document.getElementById("errormsg").innerHTML = response["message"];
            }
        }
    };
    xhr.send(fd);
});
