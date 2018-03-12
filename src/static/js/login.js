var username;
var password;

function login() {
    document.getElementById('login').classList.add('is-loading')

    username = document.getElementById('username').value
    password = document.getElementById('password').value

    var hash = CryptoJS.SHA256(CryptoJS.SHA256(password));
    console.log(hash)

    var data = "username=" + username + "&password=" + hash;

    var request = new XMLHttpRequest();
    request.open('POST', '/login', true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(data);
}