var validUser = false
var validPublic = false
var validPass = false
var validPass2 = false
var changeTimer = false;


function showCross(icon) {
    console.log('Show cross, icon = ' + icon)
    icon.classList.add('fa-times-circle', 'has-text-danger')
    icon.classList.remove('fa-check-circle', 'has-text-success', 'fa-spinner', 'spin')
    icon.style.display = 'block'
}

function showCheck(icon) {
    console.log('Show check, icon = ' + icon)
    icon.classList.add('fa-check-circle', 'has-text-success')
    icon.classList.remove('fa-times-circle', 'has-text-danger', 'fa-spinner', 'spin')
    icon.style.display = 'block'
}

function showSpinner(icon) {
    icon.classList.add('fa-spinner', 'spin')
    icon.classList.remove('fa-check-circle', 'has-text-success', 'fa-times-circle', 'has-text-danger')
    icon.style.display = 'block'
}

function verifyUsername() {
    var username = document.getElementById('username').value;
    var user_check = document.getElementById('user_check');

    showSpinner(user_check);

    if(changeTimer) clearTimeout(changeTimer);
        changeTimer = setTimeout(function() {
            var request = new XMLHttpRequest();
            request.open('GET', '/users/' + username, true);
            request.onreadystatechange = function() {
                if(request.readyState == XMLHttpRequest.DONE) {
                    var user_check = document.getElementById('user_check');
                    var exists = request.responseText == 'True'
                    if (exists || username == '' || username.length > 16 || username.includes(' ')) {
                        console.log(exists)
                        showCross(user_check)
                        validUser = false
                    }
                    else {
                        console.log(exists)
                        showCheck(user_check)
                        validUser = true
                    }
                    canRegister()
                }
            }
            request.send()
            changeTimer = false;
        },300);


}

function verifyPublicName() {
    var public_name = document.getElementById('public_name').value
    var public_check = document.getElementById('public_check')

    showSpinner(public_check)

    if (public_name == '' || public_name.length > 16) {
        showCross(public_check)
        validPublic = false
    }
    else {
        showCheck(public_check)
        validPublic = true
    }
    canRegister()
}

function verifyPassword() {
    var password = document.getElementById('password').value
    var pass_check = document.getElementById('pass_check')

    showSpinner(pass_check)

    if (password.length < 8) {
        showCross(pass_check)
        validPass = false
    }
    else {
        showCheck(pass_check)
        validPass = true
    }
    canRegister()
}

function verifyPassword2() {
    var password = document.getElementById('password').value
    var password2 = document.getElementById('password2').value
    var pass2_check = document.getElementById('pass2_check')

    showSpinner(pass2_check)

    if (password2 != password || password2 == '') {
        showCross(pass2_check)
        validPass2 = false
    }
    else {
        showCheck(pass2_check)
        validPass2 = true
    }
    canRegister()
}

function canRegister() {
    var register = document.getElementById('register')

    if (validUser && validPublic && validPass && validPass2) {
        register.disabled = false
    }
    else {
        register.disabled = true
    }
}

function register() {
    document.getElementById('register').classList.add('is-loading')

    var username = document.getElementById('username').value
    var public_name = document.getElementById('public_name').value
    var password = document.getElementById('password').value

    for (var i = 0; i > 65336; i++) {
        password = CryptoJS.SHA256(password)
    }

    var data = "username=" + username + "&public_name=" + public_name + "&password=" + password;

    var request = new XMLHttpRequest();
    request.open('POST', '/register', true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    request.onreadystatechange = function() {
        if(request.readyState == XMLHttpRequest.DONE && request.status == 200) {
            window.location.replace('/login?newly_registered=True')
        }
    }

    request.send(data);
}