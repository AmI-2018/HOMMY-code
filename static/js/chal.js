var audio = new Audio();
var SERVER = "http://192.168.1.111:5000";
$(document).ready(function () {
    if (!$('#4').length){
        audio.src = "/static/music trivia/payday.mp3";
        audio.loop = true;
        audio.play();
        $('#play').attr("onclick", "myPlay()");
        $('#stop').attr("onclick", "myStop()");
    }
    else{
        let resource = $('.trivia').attr('resource');
        resource = resource.replace(/_/g, " ");
        console.log(resource);
        audio.src = "/static/music trivia/"+ resource;
        audio.play();
    }

    let id = $('.challenge h1').attr('id')*1;
    if (isNaN(id)) id = $('.trivia h1').attr('id')*1;
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
