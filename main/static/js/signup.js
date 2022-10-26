function validate_email(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function validate_phone_number(phone_number) {
    var re = /^0\d{9}$/;
    return re.test(String(phone_number));
}

function validate_password(password) {
    // min 8, just characters and numbers
    var re = /^[a-zA-Z0-9!@#$%^&*()_+]{8,}$/;
    return re.test(String(password));
}

function validate_confirm_password(password, confirm_password) {
    return password == confirm_password;
}


document.getElementById("btn-signup").addEventListener("click", function () {

    document.getElementById("errormsg").innerHTML = "";
    document.getElementById("successmsg").innerHTML = "";

    var email = document.getElementById("email").value;
    var phone = document.getElementById("phone").value;
    var password1 = document.getElementById("password1").value;
    var password2 = document.getElementById("password2").value;

    if (!validate_email(email)) {
        document.getElementById("errormsg").innerHTML = "Email không hợp lệ";
        document.getElementById("email").focus();
        return;
    }

    if (!validate_phone_number(phone)) {
        document.getElementById("errormsg").innerHTML = "Số điện thoại không hợp lệ";
        document.getElementById("phone").focus();
        return;
    }

    if (!validate_password(password1)) {
        document.getElementById("errormsg").innerHTML = "Mật khẩu tối thiểu 8 ký tự, chỉ chứa chữ cái, số và các ký tự !@#$%^&*()_+";
        document.getElementById("password1").focus();
        return;
    }

    if (!validate_confirm_password(password1, password2)) {
        document.getElementById("errormsg").innerHTML = "Mật khẩu không trùng khớp";
        document.getElementById("password2").focus();
        return;
    }

    var fd = new FormData();
    fd.append("email", email);
    fd.append("phone", phone);
    fd.append("password", password1);
    fd.append("csrfmiddlewaretoken", document.getElementsByName("csrfmiddlewaretoken")[0].value);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/sign-up/", true);
    xhr.withCredentials = true;
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            var response = JSON.parse(xhr.responseText);
            if (response["success"] == true) {
                document.getElementById("successmsg").innerHTML = "Đăng ký thành công";
                setTimeout(function () {
                    let url = new URL(window.location.href);
                    let next = url.searchParams.get("next") || "/";
                    window.location.href = next;
                }, 2000);
            } else {
                document.getElementById("errormsg").innerHTML = response["message"];
            }
        }
    };
    xhr.send(fd);
});

// Language: javascript
// Path: main\static\js\login.js
function validate_email(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function validate_password(password) {
    // min 8, just characters and numbers
    var re = /^[a-zA-Z0-9]{8,}$/;
    return re.test(String(password));
}

document.getElementById("btn-login").addEventListener("click", function () {

    document.getElementById("errormsg").innerHTML = "";
    document.getElementById("successmsg").innerHTML = "";

    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    if (!validate_email(email)) {
        document.getElementById("errormsg").innerHTML = "Email không hợp lệ";
        document.getElementById("email").focus();
        return;
    }

    if (!validate_password(password)) {
        document.getElementById("errormsg").innerHTML = "Mật khẩu tối thiểu 8 ký tự, chỉ chứa chữ cái và số";
        document.getElementById("password").focus();
        return;
    };
    xhr.send(fd);
});