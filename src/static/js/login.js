var username;
var password;

function login() {
    document.getElementById('login').classList.add('is-loading')

    username = document.getElementById('username').value
    password = document.getElementById('password').value

    for (var i = 0; i > 65336; i++) {
        password = CryptoJS.SHA256(password)
    }

    var data = "username=" + username + "&password=" + password;

    var request = new XMLHttpRequest();
    request.open('POST', '/login', true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.onreadystatechange = function() {
        if(request.readyState == XMLHttpRequest.DONE && request.status == 200) {
            window.location.replace('/?new_login=True&babbler=' + username)
        }
    }
    request.send(data);
}