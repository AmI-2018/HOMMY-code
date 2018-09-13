var SERVER = "http://192.168.1.106:5000";
var audio = new Audio();
$(document).ready(function(){
  audio.src = "/static/sound effects/ding.mp3";
  demo();
});

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function demo() {
  await sleep(3000);
  playSound();
  var players = $(".ranking li");
  var n = $(".ranking").attr("n_players")*1;

  for(let i = 0; i<n; i++){
    let toadd= players.attr("toadd")*1;
    let old = $("#score"+(i+1)).text()*1
    $("#score"+(i+1)).text((old + toadd));
    players = players.next();
  }

  $.get({"url": SERVER + "/updateScores"});
}

async function playSound(){
  audio.play();
}
