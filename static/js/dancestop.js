$(document).ready(function(){
  demo();
});

async function demo(){
  for(var i =5; i>0; i--){
    $("#countdown").text(i);
    await sleep(1000);
  }
  $("#init_text").hide();
  $("#dance_img").attr("src","/static/img/dancingman.gif")
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}