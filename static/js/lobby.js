var SERVER = "http://192.168.1.102:5000";
$(document).ready(function () {
    $.getJSON(SERVER+"/playMusic", function (data){});
});