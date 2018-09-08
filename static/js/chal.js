var audio = new Audio();
var SERVER = "http://192.168.1.102:5000";
$(document).ready(function () {
    if ($('#4').length){
        /*audio.src = "/static/music trivia/payday.mp3";
        audio.loop = true;
        audio.play();*/

        let resource = $('.trivia').attr('resource');
        resource = resource.replace(/_/g, " ");

        audio.src = "/static/music trivia/"+ resource;

        if(resource.toString() != "payday.mp3") {
            $.getJSON(SERVER+"/stopMusic", function (data){});
            audio.play();
        }
        else $.getJSON(SERVER+"/playMusic", function (data){});

        window.setTimeout(wrongAnswer, 30000);
    }

});

function wrongAnswer() {
    //Richiesta HTTP per risposta sbagliata
    let turn = $('.turn').text();
    turn = turn.replace(/ /g, '');
    turn = turn.replace("Turn:", "");
    let headers = {"authorization": turn};

    $.get({
        "url": SERVER + "/answer/4/E",
        "headers": headers,
        "contentType": "application/json",
    });
}
