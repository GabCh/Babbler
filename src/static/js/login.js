var username;
var password;

function login() {
    document.getElementById('login').classList.add('is-loading')

    username = document.getElementById('username').value
    password = document.getElementById('password').value

    for (var i = 0; i < 65336; i++) {
        password = CryptoJS.SHA256(password)
    }

    var data = "username=" + username + "&password=" + password;

    var request = new XMLHttpRequest();
    request.open('POST', '/login', true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.onreadystatechange = function() {
        if(request.readyState == XMLHttpRequest.DONE) {
            var valid = request.responseText == 'True'
            if (valid) {
                window.location.replace('/?new_login=True&babbler=' + username)
            }
            else {
                window.location.replace('/login?invalid=True')
            }
        }
    }
    request.send(data);
}