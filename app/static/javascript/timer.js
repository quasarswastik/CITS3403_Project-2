var i = 0;
var today;

function startTime()    {
    today = new Date().getTime();
    i = i + 1;
}
function removeBtn()    {
    var button = document.getElementById("timer_btn");
    button.parentNode.removeChild(button);
}

function time() {

    if (i == 0) {
        startTime();
        removeBtn()
    }

    var now = new Date().getTime();

    var distance = now - today;
    console.log(now)
    console.log(today)
    console.log(distance);

    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
    document.getElementById("timer").innerHTML = hours + "h " + minutes + "m " + seconds + "s ";
    var t = setTimeout(time, 500);
}