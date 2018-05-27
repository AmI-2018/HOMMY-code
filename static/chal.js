var audio = new Audio();
$(document).ready(function () {
    audio.src = "/static/Hall Of Fame.mp3";
    audio.loop = true;
    audio.play();
    $('#play').attr("onclick", "myPlay()");
    $('#stop').attr("onclick", "myStop()");
});

function myStop() {
    audio.pause();
}

function myPlay() {
    audio.play();
}
