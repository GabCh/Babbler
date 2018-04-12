function showBabblesTab() {
    document.getElementById('tab-followers').classList.remove('is-active')
    document.getElementById('tab-subscriptions').classList.remove('is-active')
    document.getElementById('tab-babbles').classList.add('is-active')
    displayBabbles()
}

function showFollowersTab() {
    document.getElementById('tab-subscriptions').classList.remove('is-active')
    document.getElementById('tab-babbles').classList.remove('is-active')
    document.getElementById('tab-followers').classList.add('is-active')
    displayFollowers()
}

function showSubscriptionsTab() {
    document.getElementById('tab-followers').classList.remove('is-active')
    document.getElementById('tab-babbles').classList.remove('is-active')
    document.getElementById('tab-subscriptions').classList.add('is-active')
    displaySubscriptions()
}

function displayBabbles() {
    document.getElementById('followers').style.display = 'none'
    document.getElementById('subscriptions').style.display = 'none'
    document.getElementById('babbles').style.display = 'block'
}

function displayFollowers() {
    document.getElementById('subscriptions').style.display = 'none'
    document.getElementById('babbles').style.display = 'none'
    document.getElementById('followers').style.display = 'block'
}

function displaySubscriptions() {
    document.getElementById('followers').style.display = 'none'
    document.getElementById('babbles').style.display = 'none'
    document.getElementById('subscriptions').style.display = 'block'
}