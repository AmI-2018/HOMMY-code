var SERVER = "http://192.168.1.111:5000";
var players = new Array();
var th1,th2,th3,eliminated, time;
var tc = 100;
var names;
$(document).ready(function(){
  if($(".fitness_chal").attr("id_chal") == "chal1"){
    let string = $(".turn").text();
    string = string.replace("Turn: ", "");
    names = string.split(" ");
    //console.log(players);
    $(".turn").remove();
    let n = $(".players_list").attr("player_number")*1;
    status = initArray(n);
    th1 = initArray(n);
    th2 = initArray(n);
    th3 = initArray(n);
    time = initArray(n);
    eliminated = initArray(n);
    for(let i=0;i<n;i++){
      players[i] = randomHB();
    }
    demo(n);
  }

});

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function demo(number) {
  for(let i=0;i<180;i++){
    //console.log('Taking a break...');
    if(checkArray(eliminated, number)== number-1){
      let winners = findWinners(eliminated,number);
      for(let j = 0; j<winners.length; j++){
        let id = "#p" + (winners[j]+1);
        $(id).text("Winner!");
      }

      let headers = {"authorization": names[winners[0]]};
      let json = {"id": 1};
      for (let k = 0; k< number ; k++)
        json[names[k]] = time[k];
      json = JSON.stringify(json);
      //HTTP REQUEST FOR WINNERS
      $.post({
        "url": SERVER + "/challengeResult",
        "headers": headers,
        "data": json,
        "contentType": "application/json",
      });

      break;
    }
    else updateChallenge(i,number);
    await sleep(tc);
    //console.log('Two second later');
  }

}

function randomHB(){
  var player = new Array();
  for(let i=0;i<180;i++){
    player[i] = getRandomInt(70,130);
  }
  player.sort(function(a,b){return a-b;});
  return player;
}

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function updateChallenge(index, p_number){


  if(checkArray(th3,p_number) == p_number){
    $(".exercise h2").text("Burpees:");
    $("#exercise_img").attr("src","/static/img/fitness/burpees.jpg");
  }
  else if(checkArray(th2,p_number) == p_number){
    $(".exercise h2").text("Sit Ups:");
    $("#exercise_img").attr("src","/static/img/fitness/sit_ups.jpg");
  }
  else if(checkArray(th1,p_number) == p_number){
    $(".exercise h2").text("Pushups:");
    $("#exercise_img").attr("src","/static/img/fitness/pushups.jpg");
  }

  for(let i=0; i<p_number;i++){
    let id = "#p"+(i+1);
    if(eliminated[i]==0){
      let player = $(id).text(players[i][index]);

      if (players[i][index] >=120){
        eliminated[i]=1;
        $(id).parent().css("opacity","0.5");
        time[i]=index*tc/1000;
        console.log(time[i])
      }
      else if (players[i][index] >=110){
        $(id).css("color","red");
      }
      else if (players[i][index] >=100){
        th3[i]=1;
      }
      else if (players[i][index] >=90){
        $(id).css("color","orange");
          th2[i]=1;
      }
      else if (players[i][index] >=80){
          th1[i]=1;
      }
      else{
        $(id).css("color","#93DE74");
      }
    }
  }
}
function initArray(n){
  let array = new Array();
  for(let i =0; i<n; i++)
    array[i]=0;
  return array;
}
function checkArray(array,n){
  let c =0;
  for(let i =0; i<n; i++)
    if(array[i]==1) c++;
  return c;
}

function findWinners(array,n){
  let winners = new Array();
  let cnt=0;
  for(let i =0;i<n; i++)
    if(eliminated[i]==0)
      winners[cnt++]=i;

  return winners;
}
