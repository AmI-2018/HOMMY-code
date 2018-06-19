var audio = new Audio();
var SERVER = "http://192.168.1.111:5000";
$(document).ready(function () {
    if (!$('#4').length){
        audio.src = "/static/Hall Of Fame.mp3";
        audio.loop = true;
        audio.play();
        $('#play').attr("onclick", "myPlay()");
        $('#stop').attr("onclick", "myStop()");
    }


    let id = $('.challenge h1').attr('id')*1;
    $.get(SERVER+"/do/" + id, function (data) {
       $(".challenge").append("<h3>"+data+"</h3>");
    });


});

function myStop() {
    audio.pause();
}

function myPlay() {
    audio.play();
}
