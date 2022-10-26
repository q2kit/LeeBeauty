function more_products(btn) {
    var category_id = window.location.href.split("/")[3] || 0;
    var page = document.getElementById("page").value;

    fetch("/more_products/" + category_id + "/" + page)
        .then(response => response.json())
        .then(data => {
            if (data["success"]) {
                var products = data["products"];
                console.log(products);
            }
            else {
                document.getElementById("xxx").innerHTML = data["message"];
                btn.style.display = "none";
            }
        });
}

// event resize
window.addEventListener("resize", function () {
    if (window.innerWidth < 992) {
        document.getElementById("auth").style.marginLeft = "0px";
        document.getElementById("auth").style.marginTop = "10px";
        document.getElementById("auth").style.display = "inline";
    }
    else {
        document.getElementById("auth").style.marginLeft = "10px";
        document.getElementById("auth").style.marginTop = "0px";
    }
});

// if window width < 992px
if (window.innerWidth < 992) {
    document.getElementById("auth").style.marginLeft = "0px";
    document.getElementById("auth").style.marginTop = "10px";
    document.getElementById("auth").style.display = "inline";
}
else {
    document.getElementById("auth").style.marginLeft = "10px";
    document.getElementById("auth").style.marginTop = "0px";
}


function sync_cart() {
    console.log("sync_cart");
    var cart = localStorage.getItem("cart");
    if (cart) {
        var fd = new FormData();
        fd.append("cart", cart);
        fd.append("csrfmiddlewaretoken", document.getElementsByName("csrfmiddlewaretoken")[0].value);
        fetch("/sync-cart/", {
            method: "POST",
            body: fd
        })
            .then(response => response.json())
            .then(data => {
                if (data["success"]) {
                    localStorage.removeItem("cart");
                }
            });
    }
}

sync_cart();