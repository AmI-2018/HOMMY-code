var SERVER = "http://192.168.1.111:5000";
var turns=3;
var musicOn = true;
$(document).ready(function(){
    if($(".dancestopstart").attr("id_chal") == 3)
        demo();
});

async function demo(){
  for(let i =5; i>0; i--){
    $("#countdown").text(i);
    await sleep(1000);
  }
  playDance();
  $("#init_text").hide();
  for(let i =0; i<turns; i++){
      if(musicOn){
          await sleep(getRandomInt(5,15)*1000);
          stopDance();
      }
      else{
          await sleep(getRandomInt(3,8)*1000);
          playDance();
      }
  }
  finishDance()
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function playDance() {
    $.getJSON(SERVER+"/playDance", function (data){});
    $("#dance_img").attr("src","/static/img/dancingman.gif");
    musicOn = true;
}

function stopDance() {
    $.getJSON(SERVER+"/stopDance", function (data){});
    $("#dance_img").attr("src","/static/img/stop.png");
    musicOn = false;
}

function finishDance() {
    stopDance();
    let headers = {"authorization": "dancestop"};
    let json = {"id": 3};
    json = JSON.stringify(json);

    $.post({
        "url": SERVER + "/challengeResult",
        "headers": headers,
        "data": json,
        "contentType": "application/json",
    });
}