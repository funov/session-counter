async function sayHi() {
    let date = new Date()
    let response = await fetch('/api/v1/statistics/sessionCount');
    let dateResponse = await fetch(`/api/v1/statistics/sessionCount/${date.getDate()}-${date.getMonth() + 1}-${date.getFullYear()}`)
    let json
    let dateJson

    if (response.ok) {
        json = await response.json();
    } else {
        console.log("HTTP Error: " + response.status);
    }

    if (dateResponse.ok) {
        dateJson = await dateResponse.json();
    } else {
        console.log("HTTP Error: " + dateResponse.status);
    }

    let statisticsWidget = document.getElementById('statisticsWidget');

    let sessionCountDay = dateJson['sessionCount'][`${date.getDate()}.${date.getMonth() + 1}.${date.getFullYear()}`][window.location.pathname]
    let sessionCountMonth = dateJson['sessionCount'][`${date.getMonth() + 1}.${date.getFullYear()}`][window.location.pathname]
    let sessionCountYear = dateJson['sessionCount'][`${date.getFullYear()}`][window.location.pathname]

    let uniqueSessionCountDay = dateJson['uniqueSessionCount'][`${date.getDate()}.${date.getMonth() + 1}.${date.getFullYear()}`][window.location.pathname]
    let uniqueSessionCountMonth = dateJson['uniqueSessionCount'][`${date.getMonth() + 1}.${date.getFullYear()}`][window.location.pathname]
    let uniqueSessionCountYear = dateJson['uniqueSessionCount'][`${date.getFullYear()}`][window.location.pathname]

    let allSessionCount = json['sessionCount'][window.location.pathname]
    let allUniqueSessionCount = json['uniqueSessionCount'][window.location.pathname]

    statisticsWidget.innerHTML = `<h1>This page session count</h1>
<h2>All session count</h2>
<p>Session count = ${allSessionCount}</p>
<p>Unique session count = ${allUniqueSessionCount}</p>
<h2>Today session count</h2>
<p>Session count = ${sessionCountDay}</p>
<p>Unique session count = ${uniqueSessionCountDay}</p>
<h2>This month session count</h2>
<p>Session count = ${sessionCountMonth}</p>
<p>Unique session count = ${uniqueSessionCountMonth}</p>
<h2>This year session count</h2>
<p>Session count = ${sessionCountYear}</p>
<p>Unique session count = ${uniqueSessionCountYear}</p>`
}

let promise = sayHi();
setInterval(sayHi, 1000);
